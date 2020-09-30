#!/usr/bin/env python3
import fnmatch
import glob
import io
import os

all_project_files = []
longest_project_file = 0

def write_info_line(project_file, state, summary):
    message = f"[{state}] {project_file}"

    if summary:
        spacing_needed = longest_project_file - len(project_file) + 1
        message = f"{message}{' ' * spacing_needed}{summary}"

    print(message)

for project_file in glob.iglob("**/*/*dirs.proj", recursive=True):
    # Ignore non-files
    if not os.path.isfile(project_file):
        continue

    # Ignore anything that comes out of obj or bin
    if fnmatch.fnmatch(project_file, "obj/*") or fnmatch.fnmatch(project_file, "bin/*"):
        continue

    all_project_files.append(project_file)

    project_file_length = len(project_file)
    if project_file_length > longest_project_file:
        longest_project_file = project_file_length

for project_file in all_project_files:
    # Check the results
    results_file_path = project_file + ".Traversed.txt"
    expecteds_file_path = project_file + ".Expected.txt"

    if not os.path.isfile(results_file_path):
        write_info_line(project_file, "???", "There are no results (Was the project built?)")
    elif not os.path.isfile(expecteds_file_path):
        write_info_line(project_file, "???", "Expected results file missing!")
    else:
        results = []
        with io.open(results_file_path, mode='r') as f:
            for line in f:
                results.append(line.strip().replace('\\', '/'))

        expecteds = []
        with io.open(expecteds_file_path, mode='r') as f:
            for line in f:
                expecteds.append(line.strip())

        extra_results = results.copy()
        missing_results = expecteds.copy()

        for result in results:
            if result in missing_results:
                missing_results.remove(result)

        for expected in expecteds:
            if expected in extra_results:
                extra_results.remove(expected)

        num_extra_results = len(extra_results)
        num_missing_results = len(missing_results)

        if num_extra_results == 0 and num_missing_results == 0:
            write_info_line(project_file, "OK ", None)
        else:
            details = ""

            if num_missing_results > 0:
                s = 's' if num_missing_results > 1 else ''
                details = f"{num_missing_results} result{s} missing"

            if num_extra_results > 0:
                if len(details) > 0:
                    details = f"{details}, "
                s = 's' if num_extra_results > 1 else ''
                details = f"{details}{num_extra_results} unexpected result{s}"

            write_info_line(project_file, "BAD", details)

            for result in extra_results:
                print(f"    Unexpected project '{result}'")

            for result in missing_results:
                print(f"      Expected project '{result}'")
