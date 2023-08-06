class Utils {
	static formatFileSize = function(size){
	    let i = Math.floor( Math.log(size) / Math.log(1024) );
	    return size==0 ? "0B" :( size / Math.pow(1024, i) ).toFixed(2) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
	}
	
	static copyToClipboard(text, element = document.body) {
		let input = element.appendChild(document.createElement("input"));
		input.value = text;
		input.focus();
		input.select();
		document.execCommand('copy');
		input.parentNode.removeChild(input);
	}
}


class URLUtils {
	static convertParams(params){
		let ret = []
		for(let key in params){
			let value = params[key];
			ret.push(`${key}=${value}`);
		}
		return ret.join("&")
	}

	static getUrlQuery(){
		return window.location.search;
	}

	static getUrlParam(param){
		let queryString = this.getUrlQuery();
		let urlParams = new URLSearchParams(queryString)
		return urlParams.get(param);
	}

	static getHostInfo(){
		let url = new URL(window.location.href);
		return url;
	}
}


class FormUtils {
	/**
	 * 
	 * @param str selectId
	 * @param Array options
	 */
	static setSelectOptions(selectId, options){
		let select = document.getElementById(selectId);
		for(let index in options) {
            select.options[select.options.length] = new Option(options[index][1], options[index][0]);
		}
	}

	static setSelectSelectedOptionValue(elementId, optionValue){
		var expval = optionValue;
		var selobj;
		if(elementId.options) selobj = elementId;
		else selobj = document.getElementById(elementId);
		if(selobj!=null){
			for(var j=0;j<selobj.options.length;j++){
				if(selobj.options[j].selected && selobj.options[j].value!=expval) selobj.options[j].selected = false;
				else if(selobj.options[j].value==expval) selobj.options[j].selected = true;
			}
		}	
	}

	static getSelectSelectedOptionValue(elementId){
		if(elementId.options) return elementId.options[elementId.selectedIndex].value;
		return document.getElementById(elementId).options[document.getElementById(elementId).selectedIndex].value;
	}

	static getSelectSelectedOptionText(elementId){
		if(elementId.options) return elementId.options[elementId.selectedIndex].text;
		return document.getElementById(elementId).options[document.getElementById(elementId).selectedIndex].text;
	}
}