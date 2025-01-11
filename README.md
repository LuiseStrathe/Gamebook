<title>GamesBook README</title>

<h1>GAMES BOOK</h1>

<p>GamesBook is a free Flask web application. The app allows users to record analogue games they play! Their gaming records and analytics can be accessed by their whole group.</p>


<a href="gamesbook.site" target='_blank'>>>> Visit GameBook here!</a>

<br>

<div>
    <p><b>Table of Contents</b></p>
    <ul> 
        <li><a href="#gamesbook-app">GamesBook App</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
        <li><a href="#developer-information">Developer Information</a></li>
</div>

<br>

---
---

<br>



<h2>GamesBook App</h2>
<h3>Content</h3>
<p>GamesBook is a web application that allows users to record analogue games they play. The app is designed for groups of friends or families who play games together and want to keep track of their gaming records. You can simply access GameBook via the web browser on your smartphone, tablet or computer.</p>

<h3>Technical Setup</h3>
<p>The web application GamesBook is deployed on a project-dedicated Ubuntu VPS. The source code is accessible on the <a href='' target='_blank'>GitHub repository</a> and the deployment is done via SSH access. GameBook is served using Nginx and Gunicorn and built with Flask, Python, HTML, CSS and JavaScript.</p>

<h3>Privacy Policy</h3>
<p>The app is free to use and does not require any or personal data. Also your data will not be forwarded or used to any other entities or services.</p>


<br> 
<h2>Features</h2>

<h3>Game Records</h3>
<p>Logged-in users can record results of analogue games they play or played in the GameBook app. These records are stored in a database and can be accessed by the group, including analytics over all their records so far.</p>
<p>To create a record, a user can start a game session by selecting a game mode. Depending on the mode, they may need to add more information, e.g. which players will participate. During the game being open, users can enter their game results and when the game is done save the results.</p>



<h3>Game Modes</h3>

<p>Following game modes are available: </p>
<ul>
    <li><b>Rounds</b> <br>In a Rounds game, the game goes in rounds. At start the players which participate can be selected from the group. Then, in each round, all players can receive points. When a round is finished, the entries are locked and the total of all rounds up to that point is displayed. The number of rounds is not restricted and a game can be finished and saved at any round.
    <br><br><i>Note: This is the most <b>generic game mode</b> and can be used for many different actual games such as Scrabble, checkers or rolling dice.</i></li><br>
    <li><b>Puzzle</b> <br>A group can save multiple different puzzles they may undertake, including info such as number of pieces and a description to identify the actual real live puzzle. Once they completed a puzzle, a user can make a record in GameBook of the specific puzzle and the time it took for them to finish it under their alias within the group.</li><br> 
    <li><b>Yahtzee (a.k.a. Kniffel)</b> <br>Yahtzee is a dice game where the aim is to score points by rolling five dice to make certain combinations. The game can be played with up to 8 players and follwing a specific rule set. The game is played in rounds and the total score is calculated at the end of the game. The game can only be finished and saved after all rounds are played.
    </li>
    <br> 
    <li><b>Skat</b> <br><i>Not yet implemented</i></li>
</ul>


<h3>Group Accounts</h3>
<p>A group account with up to 8 players can be registered. Once the account is created, everyone with the shared credentials has full access. The group can hold up to 8 individual players, each identified by an alias (eg. their name). </p>
<p> With the group name and password a user can start a session by logging into the shared group space. There is no verification (e.g. with an email address) and therefore a the login credentials can not be retrieved after the account creation. This basic registration is due to the non-sensitivity of content and to ease the access to the side for multiple individuals.</p>



<h3>Analytics</h3>
<p>Once a game is finished, the group can access the analytics of all their games so far. The analytics include the total number of games, the total number of rounds, the total number of players and the average score per player. The analytics are displayed in a table and can be accessed by all group members when logged in.</p>

<h3>Test Mode</h3>
<p>Any visitor can access the test mode, which is a simple version of rounds mode. This option allows non-account users to get a feeling for the app experience without creating a group account. Naturally, no records will be safed and analytics are accessible.</p>

<h3>Responsive Design</h3>
<p>The web application is designed with a responsive layout, which means it can be accessed on any device, including smartphones, tablets and computers. The design is optimized for mobile devices and can be used on the go.</p>

<br> 
<h2>Project Structure</h2>
<p>The project structure of the <a href='https://github.com/LuiseStrathe/Gamebook' target='_blank'>repository</a> is as follows:</p>
<ul>
    <li><b>gamebook_app.py</b> <br> The main file of the Flask application. It contains the routes and the logic for the web application, called with Gunicorn via wsgi.py.</li>
    <li><b>templates/</b> <br> Contains the HTML templates for the web application.</li>
    <li><b>static/</b> <br> Contains the CSS and media files for the web application.</li>
    <li><b>src/</b> <br> Contains the Python source code for the web application.</li>
    <li><b>requirements.txt</b> <br> Contains the required Python packages for the web application.</li>
    <li><b>Licence</b> <br> Contains the MIT licence for the web application.</li></ul>
<p>User data is stored exclusively on the deployment server. The database is not included in the repository and is not accessible to the public.</p>

<br>
<h2>Developer Information</h2>
<p>GameBook is a free Flask web application developed by Luise Strathe. All source code has been developed without external support to showcase a personal project reference. The project is open source and can be accessed on <a href='https://github.com/LuiseStrathe/Gamebook' target='_blank'>GitHub</a>.</p>
<p>For any questions, feedback or suggestions, please contact the developer via the contact form on the <a href='https://www.datascienceportfol.io/Luise_strathe' target='_blank'>portfolio page</a>.</p>

<br>

<a href="#games-book">Back to Top</a>



