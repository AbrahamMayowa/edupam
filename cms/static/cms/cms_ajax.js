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
         var $clickButtonSign = $clickCommentButton.find('.thumped_up_sign');
         var $clickButtonSibilings = $clickCommentButton.siblings('.thump_up_count');
         
         

         
         $.ajax({
             type : 'get',
             url : url,
             success : function(data){
           //will reset the form. i need to used either django message framework or bootstrap alert here later
                if (data.thumped_up) {
                  $clickButtonSibilings.text(data.thump_up_count);
                  $clickButtonSign.text('thumped');
                  
                }
                else {
                  $clickButtonSibilings.text(data.thump_up_count);
                  $clickButtonSign.text('unthumped');
                  
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
       // serialize the form dat
         var url = $(this).attr('thump_down_url');
         var $clickCommentButton = $(this);
         var $clickButtonSign = $clickCommentButton.find('.thumped_down_sign');
         var $clickButtonSibilings = $clickCommentButton.siblings('.thump_down_count');
         
         

         
         $.ajax({
             type : 'get',
             url : url,
             success : function(data){
           //will reset the form. i need to used either django message framework or bootstrap alert here later
                if (data.thumped_down) {
                  $clickButtonSibilings.text(data.thump_down_count);
                  $clickButtonSign.text('thumped_down');
                  
                }
                else {
                  $clickButtonSibilings.text(data.thump_down_count);
                  $clickButtonSign.text('unthumped_down');
                  
                }

             },
             error : function(response){
                 
             }
         });
  });
});