function createUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const email = document.getElementById("email").value;

    if (username && password && email) {
        fetch("/create_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password,
                email: email
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("User created successfully!");
                window.location.href = "/login";
            } else {
                alert("Error creating user: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    } else {
        alert("Please fill in all fields.");
    }
}