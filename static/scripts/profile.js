<script>
const username = localStorage.getItem("username") || "Guest";
document.getElementById("username-display").innerText = username;
document.getElementById("display-username").innerText = username;
document.getElementById("display-name").innerText = username; // Placeholder for now

// Placeholder data — you can expand this later
document.getElementById("display-dob").innerText = "01/01/2010";
document.getElementById("display-favorite").innerText = "Reading";
</script>