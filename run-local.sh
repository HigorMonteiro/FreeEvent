while true; do
    python manage.py migrate --settings=api.config.settings_test
    # python manage.py collectstatic --settings=api.config.settings_test
    python manage.py runserver --settings=api.config.settings_test

    # Check the exit status of the command
    if [ $? -eq 0 ]; then
        # If the command succeeds, break out of the loop
        break
    else
        # If the command fails, display an error message
        echo "Command failed. Retrying..."
        sleep 0.5  # Add a delay between retries if desired
    fi
done
