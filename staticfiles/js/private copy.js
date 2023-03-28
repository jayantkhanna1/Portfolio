$(document).ready(function(){
    $("#folder-search").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#table_body tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });
  function open_delete_folder_modal(name_of_folder){
    document.getElementById('deletefoldermodal').style.display='block';
    document.getElementById('delete_folder_name').innerHTML=name_of_folder;
  }
  function open_edit_folder_modal(name_of_folder){
    document.getElementById('old-folder-name').value=name_of_folder;
    document.getElementById('editfoldermodal').style.display='block';
  }
  function open_static_modal(id,name,url,desc,start,end){
    document.getElementById('static-id').value=id;
    document.getElementById('static-name').value=name;  
    document.getElementById('static-url').value=url;         
    document.getElementById('static-desc').value=desc; 
    document.getElementById('static-start').value=start; 
    document.getElementById('static-end').value=end; 
  }
  function open_anim_modal(id,name,url,desc,start,end){
    document.getElementById('anim-id').value=id;
    document.getElementById('anim-name').value=name;  
    document.getElementById('anim-url').value=url;         
    document.getElementById('anim-desc').value=desc; 
    document.getElementById('anim-start').value=start; 
    document.getElementById('anim-end').value=end; 
  }
  function open_dyno_modal(id,name,url,desc,start,end){
    document.getElementById('dyno-id').value=id;
    document.getElementById('dyno-name').value=name;  
    document.getElementById('dyno-url').value=url;         
    document.getElementById('dyno-desc').value=desc; 
    document.getElementById('dyno-start').value=start; 
    document.getElementById('dyno-end').value=end; 
  }

  function close_modal(){
    document.getElementById('enter-name').style.display="none"
    document.getElementById('editfoldermodal').style.display='none';
    document.getElementById('deletefoldermodal').style.display='none';
    document.getElementById('deleducation').style.display='none';
  }
  window.onclick = function(event) {
    if (event.target == document.getElementById('editfoldermodal')) {
      document.getElementById('enter-name').style.display="none"
        document.getElementById('editfoldermodal').style.display = "none";
        document.getElementById('deletefoldermodal').style.display='none';
        document.getElementById('deleducation').style.display='none';
    }
  }
  
  
  function delete_static_modal(name){
    document.getElementById('static_del_name').innerHTML=name
  }
  function delete_anim_modal(name){
    document.getElementById('anim_del_name').innerHTML=name
  }
  function delete_dyno_modal(name){
    document.getElementById('dyno_del_name').innerHTML=name
  }