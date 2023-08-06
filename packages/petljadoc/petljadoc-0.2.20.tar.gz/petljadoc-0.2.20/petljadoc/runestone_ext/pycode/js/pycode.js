SIM_STATUS_STOPPED = 1
SIM_STATUS_PLAYING = 2
SIM_STATUS_PAUSED = 3
SIM_STATUS_FINISHED = 4

pyodideCodeList = {}

function PyodideCode (opts) {
    if (opts) {
        this.init(opts);
    }
}

PyodideCode.prototype.init = async function(opts){
	this.opts = opts
	this.id = opts.id
	this.simStatus = SIM_STATUS_STOPPED
	this.code = popAttribute(opts,'data-code',"") 
	this.originalCode = this.code
	this.imgPath = popAttribute(opts,'data-img-path',"")
	this.scale = parseFloat(popAttribute(opts,'data-scale',"1"))
	this.pythonError = false
	this.pythonErrorMsg = ""
	this.varsInputElementId = {}
	this.eventQue = []
	this.simImages = {}
	this.drawFunctions = {'circle' : this.drawCircle,
						  'box' : this.drawBox,
						  'line' : this.drawLine, 
						  'triangle' : this.drawTriangle,
						  'polyLine' : this.drawPolyLine,
						  'image' : this.drawImage,
						  'text' : this.drawText,
						  'rotate' : this.rotate,
						  'restore' : this.restore
						}
	this.generateEditorDiv()
}

PyodideCode.prototype.execDrawing = async function(){
	for(var i =0; i < this.eventQue.length; i++){
		await this.eventQue[i]()
	}
	this.eventQue = []
}

PyodideCode.prototype.setupCanvas = function() {
	// settings
	this.ctx.canvas.width = this.animation_instance.anim_context.settings.window_with_px * this.scale;
	this.ctx.canvas.height = this.animation_instance.anim_context.settings.window_height_px * this.scale;

	this.px_per_unit =  this.animation_instance.anim_context.settings.px_per_unit * this.scale
	this.animation_instance_x_min = this.animation_instance.anim_context.settings.view_box[0][0]
	this.animation_instance_y_min  =  this.animation_instance.anim_context.settings.view_box[0][1]
	this.animation_instance_height = this.animation_instance.anim_context.settings.view_box[2]
	this.update_period = this.animation_instance.anim_context.settings.update_period
	this.background_color =  this.animation_instance.anim_context.settings.background_color

	//drawing
	this.ctx.fillStyle = this.background_color
	this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
	this.animation_instance.queueFrame(); // setting up frist frame / thumbnail
	this.execDrawing()
}

PyodideCode.prototype.setPythonErrorMsg = function(errMsg){
		this.pythonError = true
		this.pythonErrorMsg = errMsg
}

PyodideCode.prototype.execPython = function(){
	pyodide.globals.the_script = this.code
	return pyodide.runPythonAsync(`
			try:
				exception_happened = True
				sys.stdout = io.StringIO()
				exec(the_script,{'animation_instance_key' : '${this.id}'})
			except Exception:
				exc_type, exc_value, exc_tb = sys.exc_info()
				error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb.tb_next))
			else:
				import simanim.pyodide.gui	
				exception_happened = False
			finally:
				if exception_happened:
					js.throwError(error_msg)
			`)
		.then(() => {				
			this.animation_instance = pyodide.globals.simanim.pyodide.gui.animation_instance &&  pyodide.globals.simanim.pyodide.gui.animation_instance[this.id] ?  pyodide.globals.simanim.pyodide.gui.animation_instance[this.id] : null ;
			this.stdout = pyodide.globals.sys.stdout.getvalue()
			this.pythonError = false;
			this.pythonErrorMsg = '';
		})
		.catch((msg) => {
			this.setPythonErrorMsg(msg);
			this.stdout = pyodide.globals.sys.stdout.getvalue()
		})
}

PyodideCode.prototype.generateHTMLForSim = function() {
	var simDiv = document.createElement('div');
	simDiv.setAttribute('class', 'modal-sim');

	var simDivContent = document.createElement('div');
	simDivContent.setAttribute('class', 'modal-content-sim');

	var simDivControls = document.createElement('div');
	simDivControls.setAttribute('class', 'sim-controls');

	var controlBtnDiv = document.createElement('div');
	controlBtnDiv.setAttribute('class', 'control-button-div');

	this.playBtn = document.createElement('button');
	this.playBtn.setAttribute('class', 'control-btn');
	this.playBtn.addEventListener('click', this.startSim.bind(this));
	this.playBtn.innerHTML = '<i class="fas fa-play"></i> PLAY';

	this.stopBtn = document.createElement('button');
	this.stopBtn.setAttribute('class', 'control-btn');
	this.stopBtn.setAttribute('disabled', 'disabled');
	this.stopBtn.addEventListener('click', this.stopSim.bind(this));
	this.stopBtn.innerHTML = '<i class="fas fa-stop"></i> STOP';

	this.pauseBtn = document.createElement('button');
	this.pauseBtn.setAttribute('class', 'control-btn d-none');
	this.pauseBtn.addEventListener('click', this.pauseSim.bind(this));
	this.pauseBtn.innerHTML = '<i class="fas fa-pause"></i> PAUSE';

	controlBtnDiv.appendChild(this.playBtn);
	controlBtnDiv.appendChild(this.pauseBtn);
	controlBtnDiv.appendChild(this.stopBtn);
	
	simDivControls.appendChild(controlBtnDiv);

	var variablesDiv = document.createElement('div');
	variablesDiv.setAttribute('class', 'sim-modal-variables');
	variablesDiv.setAttribute('id', 'variablesDiv');

	var variables = this.animation_instance.getVars();
	for (var i = 0; i < variables.length; i++) {
		if (variables[i].meta["type"] == 'InputFloat') {
			var variableLabel = document.createElement('label');
			variableLabel.setAttribute('class', 'variable-label');
			variableLabel.innerHTML = `${variables[i].name} = `;

			var max = variables[i]['meta']['limit_to']
			var step = Math.pow(10,Math.floor(Math.log10(max)-1))

			var variableInput = document.createElement('input');
			variableInput.setAttribute('type', 'number');
			variableInput.setAttribute('class', 'variable-input');	
			variableInput.setAttribute('id', this.id + '-' +i)		
			variableInput.setAttribute('value', '' + variables[i]['meta']['default']);
			variableInput.setAttribute('min',variables[i]['meta']['limit_from'])
			variableInput.setAttribute('max',variables[i]['meta']['limit_to'])		
			variableInput.setAttribute('step', step);
			variableInput.addEventListener('input',this.setGetters.bind(this))

			this.varsInputElementId[variables[i].name] = this.id + '-' +i	

			variablesDiv.appendChild(variableLabel);
			variablesDiv.appendChild(variableInput);
		}
		else {
			var variableLabel = document.createElement('label');
			variableLabel.setAttribute('class', 'variable-label');
			variableLabel.innerHTML = `${variables[i].name} = `;

			var selectInput = document.createElement('select');
			selectInput.setAttribute('class', 'variable-input')
			selectInput.setAttribute('id', this.id + '-' +i)
			selectInput.addEventListener('input',this.setGetters.bind(this))

			for (var j = 0; j < variables[i].meta.lov.length; j++) {
				var selectOption = document.createElement('option');
				selectOption.innerHTML = variables[i].meta.lov[j];
				if(variables[i].meta.lov[j] == variables[i].meta.default){
					selectOption.setAttribute('selected','selected')	
				}
				selectInput.appendChild(selectOption);
			}
			this.varsInputElementId[variables[i].name] = this.id + '-' +i

			variablesDiv.appendChild(variableLabel);
			variablesDiv.appendChild(selectInput);
		}
	}

	if(variables.length > 0){
		simDivControls.appendChild(variablesDiv);
	}
	
	var simBodyCanvasDiv = document.createElement('div');
	simBodyCanvasDiv.setAttribute('class', 'sim-modal-canvas');

	this.canvas = document.createElement('canvas');
	this.canvas.setAttribute('id', 'simCanvas-' + this.id);
	this.canvas.setAttribute('class', ' sim-canvas')
	this.ctx = this.canvas.getContext('2d');

	simBodyCanvasDiv.appendChild(this.canvas);
	simDivContent.appendChild(simDivControls);
	simDivContent.appendChild(simBodyCanvasDiv);

	simDiv.appendChild(simDivContent);
	if(this.stdout.length>0){
		var outDiv = createOutDiv(this.stdout)
		simDiv.appendChild(outDiv)
	}

	this.mainConentDiv = simDiv		
}

PyodideCode.prototype.startSim = function() {
	this.playBtn.classList.add('d-none');
	this.pauseBtn.classList.remove('d-none');
	this.stopBtn.removeAttribute('disabled');

	for (var varName in this.varsInputElementId) {
		document.getElementById(this.varsInputElementId[varName]).setAttribute('disabled','true')
	}
	this.simStatus = SIM_STATUS_PLAYING;
	this.startDrawing.call(this)
}



PyodideCode.prototype.generateEditorDiv =  function () {
	var editorDiv = document.createElement('div')
	editorDiv.setAttribute('class', 'editor col-md-12');

	var controlDiv = document.createElement('div')
	controlDiv.setAttribute('class','control-py')

	this.startButton = document.createElement('div')
	this.startButton.innerHTML = 'Покрени скрипту'
	this.startButton.setAttribute('class','btn btn-success btn-py')
	this.startButton.addEventListener('click', this.runPythonFromCode.bind(this))
	controlDiv.appendChild(this.startButton)

	this.restartButton = document.createElement('div')
	this.restartButton.innerHTML = '<i class="fas fa-fast-backward"></i>'
	this.restartButton.setAttribute('class','btn btn-success btn-reset')
	this.restartButton.addEventListener('click', () => {this.editor.doc.setValue(this.originalCode);this.restartButton.classList.remove('show')})
	controlDiv.appendChild(this.restartButton)

	var codeDiv = document.createElement('textarea');
	codeDiv.innerHTML = this.code
	
	editorDiv.appendChild(controlDiv)
	editorDiv.appendChild(codeDiv)
	this.opts.appendChild(editorDiv)

	this.editor = CodeMirror.fromTextArea(codeDiv,{
		autoRefresh: true,
	    lineNumbers: true,
        mode: 'python', 
		indentUnit: 4,
        matchBrackets: true, 
		autoMatchParens: true,
        extraKeys: { "Tab": "indentMore", "Shift-Tab": "indentLess" }
    })
	this.editor.on('change', () => {this.restartButton.classList.add('show')})
}


PyodideCode.prototype.runPythonFromCode = async function(){
	this.code = this.editor.getValue()
	if(pythonInitialized){
		await this.execPython()
		if(!this.pythonError && this.animation_instance){
			this.generateHTMLForSim()
		}
		else{
			this.generateHTMLforErrorOutput()
		}
		this.createAnimationModal()
		if(this.animation_instance)
			this.setupCanvas()

		document.getElementById('main-content').appendChild(this.modalDiv);		
		$("#simModal").on('hidden.bs.modal', function () {
			$("#simModal").remove()
			pyodide.runPythonAsync(`del simanim.pyodide.gui.animation_instance['${this.id}']`)
		.then()
		}.bind(this));
		$('#simModal').modal()
	}
}

PyodideCode.prototype.generateHTMLforErrorOutput = function(){
	var errLabel = document.createElement('label')
	errLabel.innerHTML = '<b>Error:</b>'
	var errorMsgDiv = document.createElement('textarea')
	errorMsgDiv.setAttribute('class', 'err')
	errorMsgDiv.innerHTML = this.pythonErrorMsg
	errorMsgDiv.disabled = true;
	var errorDiv = document.createElement('div')
	errorDiv.appendChild(errLabel)
	errorDiv.appendChild(errorMsgDiv)	
	var parentDiv = document.createElement('div')
	if(this.stdout.length>0){
		var outDiv = createOutDiv(this.stdout)
		parentDiv.appendChild(outDiv)
	}
	if(this.pythonErrorMsg.length>0)
		parentDiv.appendChild(errorDiv)
	this.mainConentDiv = parentDiv
}

PyodideCode.prototype.createAnimationModal = function (){
	this.modalDiv = document.createElement('div');
	this.modalDiv.setAttribute('id', 'simModal');
	this.modalDiv.setAttribute('class', 'modal');
	this.modalDiv.setAttribute('role', 'dialog');
	this.modalDiv.setAttribute('aria-hidden', 'true');

	var modalDivDialog = document.createElement('div');
	modalDivDialog.setAttribute('class', 'modal-dialog modal-dialog-centered modal-lg');
	modalDivDialog.setAttribute('role', 'document');

	var modalDivContent = document.createElement('div');
	modalDivContent.setAttribute('class', 'modal-content');


	var modalDivBody = document.createElement('div');
	modalDivBody.setAttribute('class', 'modal-body');
	modalDivBody.setAttribute('id', 'simModalBody');
	modalDivBody.appendChild(this.mainConentDiv)


	var modalDivFooter = document.createElement('div')
	modalDivFooter.setAttribute('class', 'modal-footer')

	var closeButton = document.createElement('button')
	closeButton.innerHTML = 'Затвори'
	closeButton.setAttribute('class', 'btn btn-secondary')
	closeButton.setAttribute('data-dismiss', 'modal')
	closeButton.setAttribute('type', 'button')
	
	modalDivFooter.appendChild(closeButton)

	modalDivContent.appendChild(modalDivBody);
	modalDivContent.appendChild(modalDivFooter)
	modalDivDialog.appendChild(modalDivContent);


	this.modalDiv.appendChild(modalDivDialog);
}


PyodideCode.prototype.setGetters =  function(){
	variableValues = {}
	for (var varName in this.varsInputElementId) {
		variableValues[varName] = this.varsInputElementId[varName] 
	}
	this.animation_instance.setVarGetters(variableValues) // resets the animation to the begining
	this.clearAndDraw()
}

PyodideCode.prototype.clearAndDraw =  function(){
	this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
	this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
	this.animation_instance.queueFrame();
	this.execDrawing()
}

PyodideCode.prototype.startDrawing =  function(){
	var startDrawing =  window.performance.now();
	if (!this.animation_instance.getEndAnimation() && this.simStatus == SIM_STATUS_PLAYING) {
	    this.clearAndDraw()
		var endDrawing = window.performance.now();
		//console.log('Next frame drawn in '+ (this.update_period*1000 - (endDrawing - startDrawing)/1000) +' s')
		//console.log('Frame drawn in '+(endDrawing - startDrawing)/1000+' s')
		this.timeoutFunc = setTimeout(() => {this.startDrawing.call(this)}, this.update_period*1000 - (endDrawing - startDrawing)/1000);
	}
	else if (this.animation_instance.getEndAnimation()){
		this.clearAndDraw()

		this.simStatus = SIM_STATUS_FINISHED
		this.playBtn.classList.remove('d-none');
		this.playBtn.setAttribute('disabled', 'disabled');
		this.pauseBtn.classList.add('d-none');
	
		clearTimeout(this.timeoutFunc)
	}
}

PyodideCode.prototype.cleanUp = function(){
	this.simStatus = SIM_STATUS_STOPPED
	this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
	this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height)
	this.animation_instance.resetAnimation();
	this.execDrawing()

	this.playBtn.classList.remove('d-none');
	this.playBtn.removeAttribute('disabled');
	this.pauseBtn.classList.add('d-none');
	this.stopBtn.setAttribute('disabled', 'disabled');

	for (var varName in this.varsInputElementId) {
		document.getElementById(this.varsInputElementId[varName]).removeAttribute('disabled')
	}

	clearTimeout(this.timeoutFunc);
}

PyodideCode.prototype.stopSim = function() {
	this.cleanUp()
}

PyodideCode.prototype.pauseSim = function() {
	this.playBtn.classList.remove('d-none');
	this.pauseBtn.classList.add('d-none');
	this.simStatus = SIM_STATUS_PAUSED
}

PyodideCode.prototype.queueDrawEvent = function(type, obj){
	this.eventQue.push(this.drawFunctions[type].bind(this, obj))
}

PyodideCode.prototype.scalarToPixel = function(scalar){
	return scalar * this.px_per_unit
}

PyodideCode.prototype.pointToPixel = function(point){
	var scalarPointX = this.scalarToPixel(point[0] - this.animation_instance_x_min)
	var scalarPointY = this.scalarToPixel(this.animation_instance_y_min + this.animation_instance_height - point[1])
	return [scalarPointX, scalarPointY]
}
PyodideCode.prototype.rectToPixel = function(rect){
	var xy_min = this.pointToPixel([rect.xy_min[0],rect.xy_min[1] + rect.height])
	var width = this.scalarToPixel(rect.width)
	var height = this.scalarToPixel(rect.height)
	return [xy_min, width, height]
}

PyodideCode.prototype.drawCircle = function(circle){
	this.ctx.save()
	this.ctx.strokeStyle = (circle.pen_color && circle.line_width) ? circle.pen_color : circle.fill_color
	this.ctx.lineWidth  = circle.line_width ?  this.scalarToPixel(circle.line_width)  : 1
	this.ctx.fillStyle = circle.fill_color; 
	if (this.ctx.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	var center = this.pointToPixel(circle.center)
	var radius = this.scalarToPixel(circle.radius)
	this.ctx.beginPath();
	this.ctx.arc(center[0], center[1], radius, 0, 2 * Math.PI, false);
	this.ctx.closePath();
	this.ctx.fill();
	this.ctx.stroke();
	this.ctx.restore();
}

PyodideCode.prototype.drawBox = function(rect) {
	this.ctx.save()
	this.ctx.lineWidth  = rect.line_width ?  this.scalarToPixel(rect.line_width)  : 1;
	this.ctx.strokeStyle = (rect.pen_color && rect.line_width) ? rect.pen_color : rect.fill_color;
	this.ctx.fillStyle = rect.fill_color;
	if (rect.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	var scaledRect = this.rectToPixel(rect)
	this.ctx.beginPath();
	this.ctx.rect(scaledRect[0][0], scaledRect[0][1], scaledRect[1], scaledRect[2]);
	this.ctx.closePath();
	this.ctx.fill();
	this.ctx.stroke();

	this.ctx.restore()
}

PyodideCode.prototype.drawLine = function(line) {
	this.ctx.save()
	this.ctx.strokeStyle = line.pen_color
	this.ctx.lineWidth = this.scalarToPixel(line.line_width);
	if (line.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	this.ctx.beginPath();
	var point1 = this.pointToPixel(line.point1)
	var point2 = this.pointToPixel(line.point2)
	this.ctx.moveTo(point1[0], point1[1]);
	this.ctx.lineTo(point2[0], point2[1]);
	this.ctx.stroke();
	this.ctx.restore()
}
PyodideCode.prototype.drawPolyLine = function(polyLine) {
	this.ctx.save()
	var numberOfPoints = polyLine.points.length
	if (numberOfPoints < 1) {
		return;
	}
	let points = polyLine.points
	this.ctx.strokeStyle = (polyLine.pen_color && polyLine.line_width) ? polyLine.pen_color : polyLine.fill_color;
	this.ctx.lineWidth =  polyLine.line_width ?  this.scalarToPixel(polyLine.line_width)  : 1;
	this.ctx.fillStyle = polyLine.fill_color;
	if (polyLine.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	this.ctx.beginPath();
	var scalarPointX 
	var scalarPointY 
	[scalarPointX, scalarPointY] = this.pointToPixel(points[0])
	this.ctx.moveTo(scalarPointX,scalarPointY)
	for (i = 1; i < numberOfPoints; i++) {
		[scalarPointX, scalarPointY] = this.pointToPixel(points[i])
		this.ctx.lineTo(scalarPointX,scalarPointY)
	};
	this.ctx.stroke();
	this.ctx.restore()
}
//triangle[6] canvas settings
//trinagle[0] point 1  X
//trinagle[1] point 1  Y
//trinagle[2] point 2  X
//trinagle[3] point 2  Y
//trinagle[4] point 3  X
//trinagle[5] point 3  Y
PyodideCode.prototype.drawTriangle = function(triangle) {
	this.ctx.save()
	this.ctx.strokeStyle = triangle[6].pen_color;
	this.ctx.lineWidth  = this.scalarToPixel(triangle[6].line_width);
	this.ctx.fillStyle = triangle[6].pen_color;
	if (triangle[6].line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	var point1 = this.pointToPixel([triangle[0],triangle[1]])
	var point2 = this.pointToPixel([triangle[2],triangle[3]])
	var point3 = this.pointToPixel([triangle[4],triangle[5]])
	this.ctx.beginPath();
	var path=new Path2D()
	path.moveTo(point1[0], point1[1]);
	path.lineTo(point2[0], point2[1]);
	path.lineTo(point3[0], point3[1]);
	this.ctx.fill(path);
	this.ctx.stroke();
	this.ctx.restore()
}

PyodideCode.prototype.drawImage = function(image) {
	this.ctx.save()
	return new Promise(function (resolve){
		if (image.file in this.simImages)
			resolve(image)
		else {
			this.simImages[image.file] = new Image();
			this.simImages[image.file].onload = () => {
				resolve(image)
			}
			this.simImages[image.file].src = pathJoin([this.imgPath, image.file]);
		}
		
	}.bind(this)).then((image) => {
		var xy_min = this.pointToPixel([image.xy_min[0],image.xy_min[1] + image.height])
		var width = this.scalarToPixel(image.width)
		var height = this.scalarToPixel(image.height)
		this.ctx.drawImage(this.simImages[image.file], xy_min[0], xy_min[1], width, height);
		this.ctx.restore()
	});

}

//text.position [X,Y] 

PyodideCode.prototype.drawText = function(text) {
	this.ctx.save()
	this.ctx.fillStyle = text.pen_color;
	var font_size = this.scalarToPixel(text.font_size)
	this.ctx.font = `bold ${font_size}px Courier New`;
	var position = this.pointToPixel(text.position)
	this.ctx.fillText(text.content, position[0], position[1]);
	this.ctx.restore()
}

PyodideCode.prototype.restore = function() {
	this.ctx.setTransform(1, 0, 0, 1, 0, 0);
}
//point[0] point around which we rotate
//point[1] angle
PyodideCode.prototype.rotate = function(point) {
	var scaledPoint = this.pointToPixel(point[0])
	this.ctx.translate( scaledPoint[0], scaledPoint[1]);
	this.ctx.rotate(point[1]);
	this.ctx.translate(- scaledPoint[0], - scaledPoint[1]);
}

window.addEventListener('load',function() {
		animations = document.getElementsByClassName('pycode')
		for (var i = 0; i < animations.length; i++) {
			pyodideCodeList[animations[i].id] = new PyodideCode(animations[i])	
		}		
});

function queDrawEvent(event){
	if(pyodideCodeList[event.animation_key])
		pyodideCodeList[event.animation_key].queueDrawEvent(event.type,event.object)
	else{
		simanimList[event.animation_key].queueDrawEvent(event.type,event.object)
	}
}

function createOutDiv(stdout){
	var outDiv = document.createElement('div')
	outDiv.setAttribute('class','mt-3')

	var label = document.createElement('label')
	label.innerHTML = '<b>Stdout:</b>'

	var output = document.createElement('textarea')
	output.innerHTML = stdout
	output.setAttribute('class', 'out')
	output.disabled = true

	outDiv.appendChild(label)
	outDiv.appendChild(output)
	return outDiv
}
