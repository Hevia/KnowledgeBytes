// Generate the summary data based on the results from the API

$(function (){
    ajaxReq(query);
});

function scrapeResults(scrape)
{
    var results = [];
    for (key in scrape)
    {
        if(scrape.hasOwnProperty(key))
        {
            results += "<p>"+ key + ": " + scrape[key] + "</p>";
        }
    }
    return results;
}

function test(){
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", "mock_summary_zebra.txt", false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                console(allText);
            }
        }
    }
    rawFile.send(null);
}