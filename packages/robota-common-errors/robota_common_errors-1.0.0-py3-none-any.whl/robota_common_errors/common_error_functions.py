"""These functions specifically test the common errors."""

import re
import fnmatch

from robota_core.string_processing import html_newlines, get_link
from robota_core.data_server import DataServer
from robota_common_errors.common_errors import CommonError


def wrong_use_of_spend(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Identify cases where students have misused the `/spend` command when trying to record
    time spent working on a gitlab issue.
    """
    issue_titles = []
    comment_list = []

    all_issues = data_source.issue_server.get_issues(data_source.start, data_source.end)
    for issue in all_issues:
        for comment in issue.comments:
            if "/spend" in comment.text or r"\spend" in comment.text:
                issue_titles.append(issue.link)
                comment_list.append(html_newlines(comment.text))
    if issue_titles:
        common_error.add_feedback_titles(["Issue title", "Text of comment"])
        common_error.add_feedback([issue_titles, comment_list])
    return common_error


def wrong_use_of_estimate(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Identify cases where students have misused the `/estimate` command when trying to record
    time estimates for a gitlab issue.
    """
    issue_titles = []
    comment_list = []

    all_issues = data_source.issue_server.get_issues(data_source.start, data_source.end)
    for issue in all_issues:
        for comment in issue.comments:
            if "/estimate" in comment.text or r"\estimate" in comment.text:
                issue_titles.append(issue.link)
                comment_list.append(html_newlines(comment.text))
    if issue_titles:
        common_error.add_feedback_titles(["Issue title", "Text of comment"])
        common_error.add_feedback([issue_titles, comment_list])
    return common_error


def wrong_way_merge(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Identify cases where students have merged develop into their feature branch rather than
    the feature branch into master.
    """
    for commit in data_source.repository.get_commits(data_source.start, data_source.end):
        if commit.merge_commit:
            commit_branches = []
            for branch in data_source.repository.get_branches():
                if branch.id == commit.id and branch.name.startswith('COMP23311'):
                    commit_branches.append(branch)
            if len(commit_branches) > 0:
                affected_commit_ids = [branch.id for branch in commit_branches]
                affected_commits = [data_source.repository.get_commit_by_id(commit_id)
                                    for commit_id in affected_commit_ids]

                common_error.add_feedback_titles(["Branch Name", "commit_id", "Author Name",
                                                  "Time"])
                common_error.add_feedback([[branch.name for branch in commit_branches],
                                           [commit.link for commit in affected_commits],
                                           [commit.author_name for commit in affected_commits],
                                           [commit.created_at for commit in affected_commits]])
    return common_error


def merge_remote_branch(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Identify cases where students have merged a remote tracking branch.
    They should be pulling *before* making local commits or rebasing their local
    branch onto the remote branch."""
    phrase = "Merge remote-tracking branch"
    regex = "Merge branch '.+' of https://"

    selected_commits = []
    for commit in data_source.repository.get_commits(data_source.start, data_source.end):
        if commit.merge_commit:
            if re.match(regex, commit.message) or phrase in commit.message:
                selected_commits.append(commit)
    if selected_commits:
        common_error.add_feedback_titles(['Commit', 'Message', 'Author Name', 'Commit Time'])
        common_error.add_feedback([[commit.link for commit in selected_commits],
                                   [commit.message for commit in selected_commits],
                                   [commit.author_name for commit in selected_commits],
                                   [commit.created_at for commit in selected_commits]])
    return common_error


def repeated_revert(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Identify cases where students have repeatedly attempted to revert commits. This is often
    because they think that a commit revert is like an undo command."""
    commits = data_source.repository.get_commits(data_source.start, data_source.end)

    first_words = [commit.message.split()[0].lower() for commit in commits]

    double_revert_index = []

    for i in range(len(first_words) - 1):
        if first_words[i] == "revert":
            if first_words[i+1] == "revert":
                double_revert_index.extend([i, i + 1])
    double_revert_index = sorted(list(set(double_revert_index)))
    double_revert_commits = [commits[i] for i in double_revert_index]

    if double_revert_commits:
        common_error.add_feedback_titles(['Commit', 'Message', 'Author Name', 'Commit Time'])
        common_error.add_feedback([[commit.link for commit in double_revert_commits],
                                   [commit.message for commit in double_revert_commits],
                                   [commit.author_name for commit in double_revert_commits],
                                   [commit.created_at for commit in double_revert_commits]])
    return common_error


def committing_comments(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Students often commit commented out code which is bad. This function checks the
    diffs for any java style commenting syntax."""
    commits = data_source.repository.get_commits(data_source.start, data_source.end)
    matches = []

    # While it would be fewer API calls to do a diff of all commits at once, the API refuses to
    # return the diff if it is too big. This means doing it one commit at a time is safer.
    commit_ids = []
    files = []
    line_numbers = []
    lines_commented = []
    for commit in commits:
        if commit.parent_ids:
            if len(commit.parent_ids) > 1:
                # If there is more than parent, get the merge source rather than the destination
                # to avoid double counting diffs when they are merged
                parent_id = commit.parent_ids[1]
            else:
                parent_id = commit.parent_ids[0]
            diffs = data_source.repository.compare(parent_id, commit.id)
            for diff in diffs:
                if not diff.new_file:
                    # Search for cases where there is a plus followed by either // or /*
                    matches = list(re.finditer(r"\+\s*//\s*(.*)\n", diff.diff))
                    if matches:
                        for match in matches:
                            comment_text = match.group(1)
                            original_line = re.search("\-\s*" + re.escape(comment_text), diff.diff)
                            if original_line:
                                commit_ids.append(commit.link)
                                files.append(diff.new_path)
                                line_num_in_diff = diff.diff[:match.start()].count('\n') -1
                                diff_up_to_match = diff.diff[:match.start()]
                                num_of_minus_lines = len(re.findall("^\-", diff_up_to_match, re.MULTILINE))
                                diff_header = re.search("@@ \-(\d+),", diff.diff)
                                start_line = int(diff_header.group(1))
                                line_num_in_file = start_line + line_num_in_diff - num_of_minus_lines
                                line_numbers.append(line_num_in_file)
                                lines_commented.append(comment_text)

    if commit_ids:
        common_error.add_feedback_titles(["Commit ID", "File", "Line number", "Commented code"])
        common_error.add_feedback([commit_ids, files, line_numbers, lines_commented])
    return common_error


def committing_conflict_markup(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Conflicts should be resolved before committing. Any commit conflict markup which gets
    committed shows that the conflict has not been properly resolved."""
    commits = data_source.repository.get_commits(data_source.start, data_source.end)
    selected_commits = []
    file_names = []
    line_numbers = []

    # For each commit, consider the diff with its parent
    for commit in commits:
        if commit.parent_ids:
            if len(commit.parent_ids) > 1:
                # If there is more than parent, get the merge source rather than the destination
                # to avoid double counting diffs when they are merged
                parent_id = commit.parent_ids[1]
            else:
                parent_id = commit.parent_ids[0]
            diffs = data_source.repository.compare(parent_id, commit.id)
            for diff in diffs:
                # Search for the conflict markup
                matches = list(re.finditer(r"\+\s*<<<<<<<", diff.diff))
                if matches:
                    for match in matches:
                        selected_commits.append(commit)
                        file_url = f"{commit.url.replace('commit', 'blob')}/{diff.new_path}"
                        file_names.append(get_link(file_url, diff.new_path))
                        line_numbers.append(diff.diff[:match.start()].count('\n'))

    if selected_commits:
        common_error.add_feedback_titles(['Commit id', 'File Name', 'Line number', 'Student Name',
                                          'Error Time'])
        common_error.add_feedback([[commit.link for commit in selected_commits],
                                   file_names, line_numbers,
                                   [commit.author_name for commit in selected_commits],
                                   [commit.created_at for commit in selected_commits]])
    return common_error


def confusing_branch_names(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Some branch names are obviously confusing and should be avoided.
    e.g. a local branch called origin/branch would have a remote tracking branch called
    origin/origin/branch"""
    branches = data_source.repository.get_branches()
    branch_names = [branch.name for branch in branches]
    confusing_branch_regex = ["HEAD", "origin/.*"]
    bad_branch_names = []
    for regex in confusing_branch_regex:
        r = re.compile(regex)
        bad_branch_names.extend(list(filter(r.fullmatch, branch_names)))

    if bad_branch_names:
        common_error.add_feedback_titles(["Confusing branch names"])
        common_error.add_feedback([bad_branch_names])
    return common_error


def commit_unnecessary_files(data_source: DataServer, common_error: CommonError) -> CommonError:
    """Certain files shouldn't be committed to a Git repo, and should probably be specified in a .gitignore file"""
    unnecessary_paths = ['thumbs.db', '.DS_store', '.ipynb_checkpoints/*', '*.class', '*.jar', '*.pyc']
    names_of_branches_to_check = ['master']
    files_wrongly_committed = []
    branch_committed_to = []

    for branch_name in names_of_branches_to_check:
        # branch = data_source.repository.get_branch(branch_name)
        files = data_source.repository.list_files(branch_name)
        for file in files:
            for path in unnecessary_paths:
                if fnmatch.fnmatch(file, path) and file not in files_wrongly_committed:
                    files_wrongly_committed.append(file)
                    branch_committed_to.append(branch_name)

    if files_wrongly_committed:
        common_error.add_feedback_titles(["Unnecessary file", "Committed to branch"])
        common_error.add_feedback([files_wrongly_committed, branch_committed_to])
    return common_error
