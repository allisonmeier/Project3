let data
let appearancesBarchart, wordmap, sankey, arcdiagram, circepack, piechart
let dataFilter = []
let stopwords = []

// stopwords csv file, i think this should work - yeah it works
d3.csv('../stopwords.csv') 
  .then(words => {
    words.forEach(d => {
      stopwords.push(d.all_words)
    })
  // returns an array of 7041 individual values
})


// main csv file
d3.csv('../data.csv')
  .then(_data =>{
    data = _data
    data.forEach(d => {
      d.character = d.character,
      d.dialogue = d.dialogue,
      d.season = +d.season,
      d.episode = +d.episode,
      d.ethnicity = d.ethnicity // Dane, Saxon, Scot, Briton, etc
    })
    console.log("If you're seeing this, your data is ready to roll")

    /* this will be great!!! */

    wordmap = new WordMap({
      parentElement: '#word-map',
    }, data)
    wordmap.initVis()

    /*appearancesBarchart = new Barchart({
      parentElement: '#words-by-char-barchart',
    }, data)
    appearancesBarchart.updateVis()*/







  })

  .catch(error => {console.log(error)})


function filterData() {
  if (dataFilter.length == 0) {
    data = data;
  } else {
      // this is a problem for future Allison
  }

}





// generally cool example: https://pentriloquist.wordpress.com/2015/05/12/visualizing-game-of-thrones/
