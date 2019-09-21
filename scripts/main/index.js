// Homepage for KnowledgeBytes

$(function(){

    $("#searchQuery").on("keypress", function(key){
        if (key.which === 13) {
            query = JSON.stringify({ "query": $(this).val()});
            window.location.href="lecture.html";
        }
    });
    $("#searchSubmit").on('click', function (){
        query = JSON.stringify({ "query": $(this).val()});
        window.location.href="lecture.html";
    });
});
