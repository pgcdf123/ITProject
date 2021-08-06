 /**use jquery to bind event in a for loop*/
  $('.card').delegate('#zan','click',function (){
    AddFavor(this)
  })
 /**To achieve a like +1 every click*/
function AddFavor(self)
  {

    var fontSize=15;
    var top=30;
    var right=80;
    var opacity=1;
    var tag=document.createElement('span');
    $(tag).text('+1');
    $(tag).css('color','green');
    $(tag).css('position','absolute');
    $(tag).css('fontSize',fontSize+"px");
    $(tag).css('top',top+"px");
    $(tag).css('right',right+"px");
    $(tag).css('opacity',opacity);
    $(self).append(tag);
    var obj=setInterval(function ()
    {
      fontSize=fontSize+5;
      top=top-5;
      right=right-5;
      opacity=opacity-0.2;
      $(tag).css('fontSize',fontSize+"px");
      $(tag).css('top',top+"px");
      $(tag).css('right',right+"px");
      $(tag).css('opacity',opacity);
      if(opacity<0)
      {
        clearInterval(obj);
        $(tag).remove();
      }
    },100)
  }