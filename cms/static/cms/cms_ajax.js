$(document).ready(function(){
    $('.js_clap').click(function(e){
     // prevent from normal form behaviour
           e.preventDefault();
         // serialize the form dat
           var url = $(this).attr('clap_url');
           

           
           $.ajax({
               type : 'get',
               url : url,
               success : function(data){
             //will reset the form. i need to used either django message framework or bootstrap alert here later
                  if (data.successful) {
                    $('.clapCount').text(data.clap_numb)                  
                    

                  }

               },
               error : function(response){
                   
               }
           });
    });
 });



 $(document).ready(function(){
  $('.thump_up_js').click(function(e){
   // prevent from normal form behaviour
         e.preventDefault();
       // serialize the form dat
         var url = $(this).attr('thump_up_url');
         var $clickCommentButton = $(this);
         var $clickThumpUpButtonSign = $clickCommentButton.find('.thumped_up_sign');
         var $clickThumpUpButtonSiblings = $clickCommentButton.siblings('.thump_up_count');
         var $clickThumpDownButtonSiblings = $clickCommentButton.siblings('.thump_down_count');
         var $clickThumpDownButtonSign = $clickCommentButton.find('.thumped_down_sign');
         console.log($clickCommentButton.siblings());
         
         
         

         
         $.ajax({
             type : 'get',
             url : url,
             success : function(data){
           //will reset the form. i need to used either django message framework or bootstrap alert here later
                console.log(data.thump_up_count);
                if (data.thumped_up) {
                  $clickThumpUpButtonSiblings.text(data.thump_up_count);
                  $clickThumpUpButtonSign.text('thumped');
                  $clickThumpDownButtonSiblings.text(data.thump_down_count);
                  $clickThumpDownButtonSign.text('unthumped');
                  
                }
                else {
                  $clickThumpUpButtonSiblings.text(data.thump_up_count);
                  $clickThumpUpButtonSign.text('unthumped');
                  $clickThumpDownButtonSiblings.text(data.thump_down_count);
                  $clickThumpDownButtonSign.text('thumped');
                  
                }

             },
             error : function(response){
                 
             }
         });
  });
});



$(document).ready(function(){
  $('.thump_down_js').click(function(e){
   // prevent from normal form behaviour
         e.preventDefault();
       // serialize the form 
       
         var url = $(this).attr('thump_down_url');
         var $clickCommentButton = $(this);
         var $clickThumpDownButtonSign = $clickCommentButton.find('.thumped_down_sign');
         var $clickThumpDownButtonSiblings = $clickCommentButton.siblings('.thump_down_count');
         var $clickThumpUpButtonSiblings = $clickCommentButton.siblings('.thump_up_count');
         var $clickThumpUpButtonSign = $clickCommentButton.find('.thumped_up_sign');
         
         

         
         $.ajax({
             type : 'get',
             url : url,
             success : function(data2){
           //will reset the form. i need to used either django message framework or bootstrap alert here later
                console.log(data2.thump_down_count);
                if (data2.thumped_down) {
                  $clickThumpDownButtonSiblings.text(data2.thump_down_count);
                  $clickThumpDownButtonSign.text('thumped_down');
                  $clickThumpUpButtonSiblings.text(data2.thump_up_count);
                  $clickThumpUpButtonSign.text('unthumped');
                  
                }
                else {
                  $clickThumpDownButtonSiblings.text(data2.thump_down_count);
                  $clickThumpDownButtonSign.text('thumped_down');
                  $clickThumpUpButtonSiblings.text(data2.thump_up_count);
                  $clickThumpUpButtonSign.text('unthumped');
                  
                }

             },
             error : function(response){
                 
             }
         });
  });
});

$(document).ready(function(){
  setTimeout(function(){
    $('.message').fadeOut('slow');
  }, 10000);

  $('.del_msg').on('click', function(){
    $('.del_msg').parent().attr('style', 'display:none;');
  })

});