#!/bin/sh

echo "Waiting for Galaxy..."
until [ "$(curl -s -o /dev/null -w '%{http_code}' ${GALAXY_URL:-nginx}/api/users/current\?key\=${GALAXY_DEFAULT_ADMIN_KEY:-fakekey})" -eq "200" ] && echo Galaxy started; do
  sleep 1;
done;

export BIOBLEND_GALAXY_URL=${GALAXY_URL:-http://nginx}
export BIOBLEND_GALAXY_API_KEY=${GALAXY_DEFAULT_ADMIN_KEY:-fakekey}
export BIOBLEND_TEST_JOB_TIMEOUT=${BIOBLEND_TEST_JOB_TIMEOUT:-240}

# default skip tests
DEFAULT_SKIP_TESTS="not test_rerun_and_remap and not test_create_quota and not test_get_quotas and not test_delete_undelete_quota and not test_update_quota and not test_update_non_default_quota and not test_upload_from_galaxy_filesystem and not test_get_datasets and not test_datasets_from_fs and not test_existing_history and not test_new_history and not test_params and not test_tool_dependency_install and not test_download_history and not test_export_and_download and not test_cancel_invocation and not test_run_step_actions and not test_extract_workflow_from_history"

EXTRA_SKIP_TESTS_BIOBLEND=${EXTRA_SKIP_TESTS_BIOBLEND:-""}

# Combine default skip tests with extra skip tests, if provided
SKIP_TESTS="$DEFAULT_SKIP_TESTS"
[ -n "$EXTRA_SKIP_TESTS_BIOBLEND" ] && SKIP_TESTS="$SKIP_TESTS and $EXTRA_SKIP_TESTS_BIOBLEND"

tox -e py310 -- -k "$SKIP_TESTS"
