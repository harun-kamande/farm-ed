
$(document).ready(function(){
    // Wait for 4 seconds using setTimeout
    setTimeout(function(){
        // After 4 seconds, change the text of the element with id "myElement"
        // i am using this in login incase of wrong credentials
        $("#flash-message").text("");
    }, 4000);
});

// this is a javascript that will pop after the post is deleted by the poster
function deleted_alert(){
    window.alert("Post was deleted successifully")
}


function toggleVisibility(button) {
    let givingDiv = button.nextElementSibling;
    if (givingDiv.style.display === "none" || givingDiv.style.display === "") {
        givingDiv.style.display = "block";
        button.innerHTML = "Hide Replies";
    } else {
        givingDiv.style.display = "none";
        button.innerHTML = "View Replies";
    }
    
}

function togglereplyVisibility(button) {
    let givingDiv = button.nextElementSibling;
    if (givingDiv.style.display === "none" || givingDiv.style.display === "") {
        givingDiv.style.display = "block";
        button.innerHTML = "Reply";
    } else {
        givingDiv.style.display = "none";
        button.innerHTML = "Reply";
    }
    
}

function toggle_editVisibility(button) {
    let givingDiv = button.nextElementSibling;
    if (givingDiv.style.display === "none" || givingDiv.style.display === "") {
        givingDiv.style.display = "block";
        button.innerHTML = "Hide Edit";
    } else {
        givingDiv.style.display = "none";
        button.innerHTML = "Edit";
    }
    
}

document.addEventListener("DOMContentLoaded", function() {
    let buttons = document.querySelectorAll("button.toggle-btn");
    buttons.forEach(function(button) {
        button.addEventListener("click", function() {
            toggleVisibility(this);
        });
    });
});


