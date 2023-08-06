class App {
	/**
	 * @param jQueryInstance: Object
	 * @param mainCOntainerId: String
	 * @param config: Object
	 */
	constructor(jQueryInstance, mainCOntainerId, config){
		this.$ = jQueryInstance;
		this.$mainContainer = this.$(`#${mainCOntainerId}`);
		this.config = config;

		this.dirContext = URL.getUrlParam("context") || "";

		this._renderUI();
		this._initUI();
		this._renderFileList();
	}

	_renderUI(){
		let ui = `
		<div class="app">
			<div id="file-list"></div>
		</div>`
		this.$mainContainer.html(ui);
	}

	_initUI(){
	}

	_renderFileList(){
		this._callApi("GET", `dir/${this.dirContext}`, {}, (data)=>{
			if(data){
				let container = this.$mainContainer.find("#file-list"); 
				container.empty();
				this.dirContext = data.context;
				for(let item of data.result) {
					let type = item.type;
					let filename = item.name;
					let filepath = item.path;
					let filesize = Utils.formatFileSize(item.size);
					let token = item.token;

					let html = "";
					if(type == "file") {
						if(token){
						html =
							`<div class="file-container">` +
								`<div class="file-wrapper">` +
									`<div class="file"><a href="/share/${filepath}?token=${token}" target="_blank">${filename}</a></div>` +
									`<div class="filesize">${filesize}</div>` +
								`</div>` +
								`<div class="image-buttons">` +
									`<button class="image-button-new-token" data-param="${filepath}">New token</button>` +
									`<button class="image-button-delete-token" data-param="${filepath}">Delete token</button>` +
									`<button class="image-button-delete-file" data-param="${filepath}">Delete file</button>` +
								`</div>` +
							`</div>`
						} else {
							html =
							`<div class="file-container">` +
								`<div class="file-wrapper">` +
									`<div class="file">${filename}</div>` +
									`<div class="filesize">${filesize}</div>` +
								`</div>` +
								`<div class="file-buttons">` +
									`<button class="image-button-new-token" data-param="${filepath}">New token</button>` +
									`<button class="image-button-delete-token" data-param="${filepath}">Delete token</button>` +
									`<button class="image-button-delete-file" data-param="${filepath}">Delete file</button>` +
								`</div>` +
							`</div>`
						}
					} else {
						html =
							`<div class="dir-container">` +
								`<div class="dir">` +
									`<a href="?context=${filepath}">${filename}</a>` +
								`</div>` +
								`<div class="image-buttons">` +
									`<button class="image-button-delete-dir" data-param="${filepath}">Delete dir</button>` +
								`</div>` +
							`</div>`
					}
					container.append(html);
				}
				// add buttons handlers
				this.$mainContainer.find(".image-button-new-token").click((event)=>{
					let param = event.target.getAttribute("data-param");
					this._callApi("POST", `token/${param}`, {}, (data)=>{this._renderFileList()})
				});
				this.$mainContainer.find(".image-button-delete-token").click((event)=>{
					let param = event.target.getAttribute("data-param");
					this._callApi("DELETE", `token//${param}`, {}, (data)=>{this._renderFileList()})
				});
				this.$mainContainer.find(".image-button-delete-file").click((event)=>{
					let param = event.target.getAttribute("data-param");
					this._callApi("DELETE", `file/${param}`, {}, (data)=>{this._renderFileList()})
				});
				this.$mainContainer.find(".image-button-delete-dir").click((event)=>{
					let param = event.target.getAttribute("data-param");
					this._callApi("DELETE", `dir/${param}`, {}, (data)=>{this._renderFileList()})
				});
			}
		});
	}

	_callApi(method, command, params = {}, callback = null){
		let _this = this;
		let getParams = URL.convertParams(params);
		let apiCall = getParams == "" ? `${this.config.apiURL}/${command}` : `${this.config.apiURL}/${command}?${getParams}`;
		this.$.ajax({
			url: apiCall,
			method: method,
			success: (data)=>{
				if(data.status === false){
					alert(`Error: ${data.message}`);
				}
				if(callback) callback(data);
			}
		});
	}

}
