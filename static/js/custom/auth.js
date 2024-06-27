
$(document).ready(function(){
    // Wait for 4 seconds using setTimeout
    setTimeout(function(){
        // After 4 seconds, change the text of the element with id "myElement"
        $("#flash-message").text("");
    }, 4000);
});

function deleted_alert(){
    window.alert("Post was deleted successifully")
}

function reply_function(){
    document.getElementById("replyform").style.display='block'
}

function editing(){
   value=document.getElementById("post_id").value
    document.getElementById("edit").style.display="block";
    alert (value)
}




