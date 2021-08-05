
function checkUsername(){
    var username = document.getElementById("username").value;
    var reg_username = /^\w{6,14}$/;
    var flag = reg_username.test(username);
    var s_username = document.getElementById("s_username");
    if(flag){
        s_username.innerHTML = "<img height='25' src='' > "
    }else {
        s_username.innerHTML = "the length should between 6 - 14"
    }
    return flag;
}

function checkPassword(){
    var password = document.getElementById("password").value;
    var reg_password = /^\w{8,16}$/;
    var flag = reg_password.test(password);
    var s_password = document.getElementById("s_password");
    if(flag){
        s_password.innerHTML = '';
    }else {
        s_password.innerHTML="the length should between 8 - 16"
    }
    return flag;
}

$(function(){
    $("user_form").submit(function(){
        if(checkUsername()&&checkPassword()){

        }
    });
    return false;
})
function preCheck(){
   var username = document.getElementById("username").value;
   $.ajax({
       type: 'POST',
       url: '/rango/pre_check_username',
       data: {username:username},
       success: function (data){
           if(data.flag){
               document.getElementById('s_username').innerText = 'the username has already existed'
           }else {
               document.getElementById('s_username').innerText = 'you can use this username'
           }
       }
   })
}

