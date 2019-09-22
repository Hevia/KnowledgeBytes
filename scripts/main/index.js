// Homepage for KnowledgeBytes

$(function(){
    var result={}, summary;
    $("#searchQuery").on("keypress ", function(key){
        if (key.which === 13) {
            ajaxReq(JSON.stringify({ "query":$(this).val()})).done(function(data){
                result = data;
                console.log(result)
                summary = scrapeResults(result);   
            console.log(summary);
            $("#summary").html(summary);        
        })
    }
    });

    $("#searchSubmit").on('click', function (){
        ajaxReq(JSON.stringify({ "query": $(this).val()})).done(function(data){
            result = data;
            console.log(result)
            summary = scrapeResults(result);   
            console.log(summary);
            $("#summary").html(summary);
            })
        });
    });

function ajaxReq(data) {
    
    return $.ajax({
        url: "http:localhost:5000/search_query",
        contentType: 'application/json; charset=UTF-8',
        type: "POST",
        data: data,
    });
}

function scrapeResults(scrape)
{
   
var scraped = JSON.parse(scrape);
var results;
for (prop in scraped)
{
    if(scraped.hasOwnProperty(prop))
        results += "<p>"+prop +": " +  scraped[prop] + "</p>";  
}
return results;
}

