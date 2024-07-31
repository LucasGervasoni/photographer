var infoBtn = document.getElementById("view");

infoBtn.addEventListener("click",function(){
  var info = document.getElementById("listInfo");

  if(info.classList.contains('d-none')){
    info.classList.remove('d-none')
  }else{
    info.classList.toggle('d-none')
  }
});
