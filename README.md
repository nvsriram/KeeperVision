# KeeperVision

## Instructions on running locally

1. Ensure python is installed
2. Run `pip install -r requirements.txt` to install all dependencies<br />
   **NOTE:** Recommended to use venv before installing dependencies. See below for details on how to set it up
3. Run the Flask app using `python app.py`. This will run the app on debug mode on the server's IP
4. **NOTE**: Ensure the Flask app and the client are in the same WLAN to be able to connect to the server's IP as it is otherwise considered a private IP address

**[Optional]** To use venv:

1. Run `python -m venv <path-to-env>` to create virtual environment
2. To activate the virtual environment:

   - If on Windows, run: `<path-to-env>/Scripts/activate`
   - If on MacOS, run: `source <path-to-env>/bin/activate`

3. Run Step 2 to install all dependencies
