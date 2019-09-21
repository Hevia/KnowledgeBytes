// Generate the summary data based on the results from the API

$(function (){
var result = scrapeResults(1);

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
    //var obj = {
    //}
    // if(option === 1)
    // {
    //  obj = {
    //         title: scrape.title,
    //         date: {
    //             start: scrape.start,
    //             end: scrape.end
    //         },
    //         location: scrape.location,
    //         summary: scrape.summary,
    //         actors: {
    //             Faction1:scrape.Faction1,
    //             Faction2: scrape.Faction2
    //         },
    //         result: scrape.result,
    //         similar: scrape.similar
    //     } 
    // }

    // else if(option === 2)
    // {
    // obj = {
    //         title: scrape.title,
    //         science_name: scrape.science_name,
    //         classification:{
    //             Kingdom: scrape.Kingdom,
    //             Phylum: scrape.Phylum,
    //             Class: scrape.Class
    //         },
    //         Biological_properties:{
    //             lifespan: scrape.lifespan,
    //             Length: scrape.Length,
    //             Weight: scrape.Weight
    //         },
    //         summary: scrape.summary,
    //         similar: scrape.similar
    //     } 
    // }
}