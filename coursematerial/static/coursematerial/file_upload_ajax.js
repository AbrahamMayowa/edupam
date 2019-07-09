
//checking if client is successfully access file ajax view before the page will auto redirect
var check_connectivity = {
  is_internet_connected: function() {
      return $.get({
          url: $('button').attr('ajax_view_url'),
          dataType: 'text',
          cache: false
      });
  },
};

$(function () {
  //to ensure that user connect to internet before upload window will pop up
    $(".js-upload-photos").click(function(){
        $("#fileupload").click();});

    var redirect_url = $('button').attr('redirect_url');
   
    $("#fileupload").fileupload({
      dataType: 'json',
      sequentialUploads: true,  /* 1. SEND THE FILES ONCE */
      start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
        $("#modal-progress").modal("show");
      },
      stop: function (e, data) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
        $("#modal-progress").modal("hide");
        check_connectivity.is_internet_connected().done(function() {
    //if the resources is accessible
         window.location.replace(redirect_url);

})
       
      },
      progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      },
      done: function (e, data) {
        if (data.result.successful) {
          $("#success_alert").text(data.result.message);
          }
        else {
          $('#success_alert').text(data.result.message);
        }},
      fail: function(e){
        $('#success_alert').text('Error');
      },
  
    });
  
  });

