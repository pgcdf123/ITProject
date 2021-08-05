$(function(){
    $("#bt_sub").click(function(){
        var uname = document.getElementById("uname").value;
        var pwd= document.getElementById("pwd").value;
        $.post("rango/login/",{username:uname,password:pwd},function(data){
                console.log(data)
                // $("#errorMsg").removeClass(".hidde")
        });
    })
})