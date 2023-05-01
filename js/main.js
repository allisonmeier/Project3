let data
let appearancesBarchart, wordmap, sankey, chordDiagram, circepack, piechart
let dataFilter = []
let stopwords = []
const seasonSelector = d3.select('#seasonSelector')
const divContainer = d3.select('#container')

// top 20 speakers
let mainCharacters =['Uhtred', 'Edward', 'Finan', 'Brida', 'Aethelhelm', 'Stiorra', 
  'Aethelstan', 'Sihtric', 'Aelswith', 'Sigtryggr', 'Pyrlig', 'Beocca', 'Aldhelm', 
  'Alfred', 'Aethelflaed', 'Eadith', 'Leofric', 'Rognvaldr', 'Bresal', 'Osferth']

// main csv file
d3.csv('../data.csv')
  .then(_data =>{
    data = _data
    data.forEach(d => {
      d.character = d.character,
      d.dialogue = d.dialogue,
      d.season = d.season,
      d.episode = +d.episode,
      d.ethnicity = d.ethnicity // Dane, Saxon, Scot, Briton, etc
    }) 

    /* Ethnicity:
      Saxon : '#F25041'
      Irish : '#38B000'
      Dane-Saxon : '#8C1F66'
      Mercian : '#33A6A6'
      Dane : '#323673'

    */


    d3.csv('../stopwords.csv') 
      .then(words => {
        words.forEach(d => {
          stopwords.push(d.all_words)
        })
      // returns an array of 7041 individual word values, pre-filtering
      console.log("If you're seeing this, your data is ready to roll")
      
      wordmap = new WordMap({
        parentElement: '#word-map',
      }, data)
      //wordmap.initVis()

      appearancesBarchart = new Barchart({
        parentElement: '#words-by-char-barchart',
      }, data)
      appearancesBarchart.updateVis()

      chordDiagram = new ChordDiagram({
        parentElement: '#chord-diagram',
      }, data)
      //chordDiagram.initVis()

      /*sankey = new SankeyDiagram({
        parentElement: '#sankey-diagram',
      }, data)
      sankey.initVis()*/

      /*hierarchyMap = new CirclePack({
        parentElement: '#hierarchy-map',
      })*/


            
      filterData(seasonSelector.property('value'))

      seasonSelector.on('change', () => {
        selectedSeason = d3.select(seasonSelector).property('value')
        console.log(selectedSeason)
        filterData(selectedSeason)
      })
  
  
  })

    //console.log("If you're seeing this, your data is ready to roll")
    //console.log(data)
    /* this will hopefully be great :(  */


  })

  .catch(error => {console.log(error)})


function filterData(selectedSeason) {
  console.log(selectedSeason)
  if (selectedSeason = 'all') {
    data = data;
  } else {
    let filteredData = data.filter(d => d.season == selectedSeason)
    /*divContainer.selectAll('div')
      .data(filteredData)
      .join('div')*/

      wordmap = new WordMap({parentElement: '#word-map'}, filteredData)
      appearancesBarchart = new Barchart({parentElement: '#words-by-char-barchart'}, filteredData)
      chordDiagram = new ChordDiagram({parentElement: '#chord-diagram'}, filteredData)

  }

}


// generally cool example: https://pentriloquist.wordpress.com/2015/05/12/visualizing-game-of-thrones/
