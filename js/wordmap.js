class WordMap {

    /* this should show words spoken most overall, 
    and eventually per character*/

    constructor(defaultConfig, _data) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 500,
            containerHeight: defaultConfig.containerHeight || 500,
            margin: defaultConfig.margin || {top: 5, right: 5, bottom: 5, left: 5},
        }
        this.data = _data
        this.initVis()
    }

    initVis(){
        let vis = this

        vis.width = vis.config.containerWidth + vis.config.margin.left + vis.config.margin.right
        vis.height = vis.config.containerHeight + vis.config.margin.top + vis.config.margin.bottom
    
        vis.sizeScale = d3.scaleLinear()
            .range([20, 60])     
    
        vis.svg = d3.select(vis.config.parentElement)
            .append('svg')
                .attr('width', vis.width + vis.config.margin.left + vis.config.margin.right)
                .attr('height', vis.height + vis.config.margin.top + vis.config.margin.bottom)
                //.append('g')
                //.attr('transform', `translate(${10},${10})` )
    
        vis.updateVis()

    }

    updateVis() {
        let vis = this
        vis.wordFrequencyMap = {}

        let words
        // eventually allow user to filter boring stuff in and out
        let superBoringWords = ['you', 'the', 'i', 'to', 'is', 'and', 'a', 'of', 'will', 'not', 'it', 
            'we', 'have', 'be', 'my', 'he', 'your', 'that', 'for', 'are', 'do', 'in', 'this', 'with',
            'him', 'his', 'her', 'as', 'can', 'on', 'they', 'has', 'am', 'if', 'was', 'all', 'them', 
            'but', 'would', 'what', 'me', 'no', 'there', 'who', 'at', 'our', 'did', 'so', 'from', 'im',
            'she', 'us', 'an', 'here', 'then', 'must', 'like', 'its', 'now', 'man', 'should', 'one',
            'why', 'how', 'by', 'were', 'been', 'well', 'say', 'or', 'when', 'only', 'could', 'hes',
            'too', 'their', 'than', 'just', 'youre', 'does']

        let kindaBoringWords = ['men', 'come', 'take', 'need', 'see', 'go', 'more', 'where', 'know', 
            'may', 'want', 'yes', 'let', 'make', 'get']

        vis.data.forEach(d => {
            words = d.dialogue
                .replace(/[^a-z\s]/igm,'') // replaces anything other than letters or spaces, with ''
                .toLowerCase() // makes every single letter lowercase
                .split(/\s/gm) // splits everything in the string incl long strings
                .filter(string => string) //filters out dud empties
                .filter(word => !superBoringWords.includes(word))
                .filter(word => !kindaBoringWords.includes(word))
            words.forEach(word => {
                if (!vis.wordFrequencyMap[word]) {
                    vis.wordFrequencyMap[word] = 1
                } else {
                    vis.wordFrequencyMap[word] += 1 // in stop_words???
                }  
            })
        })

        // deals with it like its an array, maps the word to its overall size in the wordmap
        vis.wordFrequency = Object.entries(vis.wordFrequencyMap).map(f => ({word:f[0], size:f[1]}))
        vis.wordFrequency.sort((a,b) => (b.size - a.size))
        vis.wordFrequency = vis.wordFrequency.slice(0,40)

        console.log(vis.wordFrequency)

        // domain of words and their corresponding sizes are referred to 
        vis.sizeValue = d => d.size
        vis.sizeScale.domain(d3.extent(vis.wordFrequency, vis.sizeValue))

        // now we make all this stuff into something visible
        vis.layout = d3.layout.cloud()
            .size([vis.width, vis.height])
            .words(vis.wordFrequency.map(d => {return {text: d.word, size: vis.sizeScale(vis.sizeValue(d))} }))
            .padding(5)
            .rotate(() => { return parseInt(Math.random() * 2) * 90; }) //{return parseInt((Math.random()*2)*90)})
            .fontSize(d => {return d.size})
            .on('end', words => draw(words) )

        vis.layout.start() // OH YEAH

        function draw(words){
            console.log(vis.layout.size())

            vis.svg
                .join('g')
                    .attr("transform", `translate(${vis.layout.size()[0]/2},${vis.layout.size()[1]/2})`)
                //.attr("transform", `translate(${vis.width / 2}, ${vis.height / 2})`)
                .selectAll('text').data(words)
                .join('text')
                    .attr('font-size', d => {return d.size})
                    .attr('text-anchor', 'middle')
                    .attr('font-family', 'sans-serif')
                    .attr('transform', d => { return `translate("${[d.x, d.y]}")rotate("${d.rotate}")` })
                    .text(d => {return d.text})
            }

    }


// WHY WONT THIS WORK ARGHHHHHHHHHHHH

}