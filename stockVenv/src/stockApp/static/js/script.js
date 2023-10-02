$(document).ready(function(){

    // -------------------- pagination setup --------------------
    $(".table").paging({limit:5});

    // -------------------- progress / page loading setup --------------------
    NProgress.start();
    NProgress.done();

    // -------------------- datetime picker / calender -------------------- 
    $(".datetimeinput").datepicker({changeYear: true, changeMonth: true, dateFormat: "yy-mm-dd"});
   
});





