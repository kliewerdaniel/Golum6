---
layout: post
title: "Running Large Language Models Locally: A Step-by-Step Guide to
  Installing Open WebUI"
date: 2024-09-13T20:19:37.442Z
---
**Introduction:**

In recent years, large language models (LLMs) have gained significant attention for their ability to process and generate human-like text. However, running these models on remote servers can be slow and unreliable due to network latency issues. On the other hand, running them locally on your machine provides a much faster and more reliable experience. 

Open WebUI is an open-source web-based interface that allows you to run and use LLMs locally without requiring extensive programming knowledge. In this guide, we will show you how to install Open WebUI and start using large language models on your computer.

**Step 1: Install Node.js and npm**

Open WebUI is built using JavaScript and requires Node.js to be installed in your machine. If you already have Node.js installed, skip to the next step. Otherwise, follow these steps:

- Go to the [official Node.js website](https://nodejs.org/en/download/) and download the latest version of Node.js for your operating system.

- Install Node.js according to the installation instructions provided in its official documentation.

Next, you need to install npm (the package manager for JavaScript), which comes bundled with Node.js. If npm is installed correctly, you can verify it by running the following command on your terminal or command prompt:
```bash
npm --version
```

**Step 2: Install Open WebUI**

To install Open WebUI, follow these steps:

- First, ensure that node and npm are updated using:
   ```bash
    npm update -g npm && npx migrate
    ```

- Next, to install open-webui package by running this command in your terminal or command prompt:
   ```bash
   npx create-webui-app
   ```
   **Note:** The `npx` binary is used here instead of the global npm package as it ensures you're using a clean version specifically created for each task without affecting your global node modules.

- After running the command, follow the instructions provided in the terminal or command prompt to customize your project. This may involve selecting an app name and choosing how you want your frontend to be generated.
   
This entire process can be simplified into a .sh (Bash shell) script:

Here's a basic `.sh` file that performs these steps for convenience:
```bash
#!/bin/bash

# Updating npm (only necessary if you haven't updated npm in a while)
npm update -g npm && npx migrate

# Install open-webui package, note: The exact command might vary slightly depending on your platform (Windows, Linux, macOS).
npx create-webui-app  # Follow prompts and customize the project as instructed.

echo "Installation completed."
```
The best way to handle this `.sh` script is by adding execution permissions with the `chmod +x install-webui.sh` command followed by `./install-webui.sh`

Remember, always run your scripts from the directory where you want the application to be installed

**Step 3: Launch Open WebUI**

To start using Open WebUI:

- First, navigate into the project folder created in step 2.
- Run:
   ```bash
   npm start
   ```
or
```bash 
npx webui start
```
depending on the package you're currently running.

You will see your local open-webui instance being listened to. By visiting http://127.0.0.1:10000 (you can find exact URL in your terminal output after running npm or npx commands) in a new browser tab, you'll be able interact with Open web-ui locally

Open WebUI comes pre-configured to support popular LLMs directly accessible through their own interfaces within webui, making it easy to use.