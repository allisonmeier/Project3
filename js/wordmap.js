class WordMap {

    /* this should show words spoken per character, 
    and maybe eventually episodes appeared in per character*/


    constructor(defaultConfig, _data) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 700,
            containerHeight: defaultConfig.containerHeight || 300,
            margin: defaultConfig.margin || {top: 5, right: 5, bottom: 20, left: 20},
        }
        this.data = _data
        this.initVis()
    }

    initVis(){
        return
    }

    updateViv() {
        return
    }

    renderVis() {

    }


}