
$(document).ready(function(){
    // Wait for 4 seconds using setTimeout
    setTimeout(function(){
        // After 4 seconds, change the text of the element with id "myElement"
        $("#flash-message").text("");
    }, 4000);
});



function feedback_submision(){
    post=document.getElementById("title").value;
    feedback=document.getElementById("post").value;

    if (feedback && post){
        window.alert("Your feedback was submited successifully!!")
    }

}



function deleted_alert(){
    window.alert("Post was deleted successifully")
}

function reply_function(){
    document.getElementById("replyform").style.display='block'
}