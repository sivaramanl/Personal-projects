# Windows spotlight collector

<b>Introduction</b>
<br>
Do you like the Windows spotlight feature? I have, for a long time. If you are wondering what it is, <a href="https://en.wikipedia.org/wiki/Windows_Spotlight">Wikipedia</a> is here to help.

The highlight of the feature is that the high definition images that are refreshed regularly. This naturally means that the images are out of reach to the end user.

This small project intends to create a means to collect the Spotlight images. Please be aware that some data might be licensed and thus this tool must be utilized with caution.

<b>Pre-requisites</b>
<br>
Python version 3.7 and higher.

<b>Instructions</b>
<ul>
  <li>Download the entire folder.</li>
  <li>Open the spotlight_config file and edit the directory to which the images are to be copied.</li>
  <li>The tool can now be configured in either of the following ways.
      <ol>
        <li>Run the setup.bat file as an Administrator. This should set up all the required configurations.
          <br>
          If this fails, utilize the second method.
        </li>
        <li>
          Open the Task Scheduler application.
          <br>
          Click on Action > Create task > Configure the following
          <br>
          &nbsp;&nbsp;&nbsp;&nbsp;>Enter the task name under General tab
          <br>
          &nbsp;&nbsp;&nbsp;&nbsp;>Create a new trigger. Beginning the task on workstation unlock is preferred.
          <br>
          &nbsp;&nbsp;&nbsp;&nbsp;>Create a new action. Add "windows_spotlight_copier.bat" as the executable script under settings.
        </li>
      </ol>
  </li>
</ul>
