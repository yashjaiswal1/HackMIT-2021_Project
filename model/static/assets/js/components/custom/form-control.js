//
// Form control
//

'use strict';

var FormControl = (function() {

	// Variables

	var $input = $('.form-control');


	// Methods

	function init($this) {
		$this.on('focus blur', function(e) {
        $(this).parents('.form-group').toggleClass('focused', (e.type === 'focus'));
    }).trigger('blur');
	}

	function handleFiles(event) {
		var files = event.target.files;
		$("#src").attr("src", URL.createObjectURL(files[0]));
		document.getElementById("audio").load();
	}
	
	document.getElementById("upload").addEventListener("change", handleFiles, false);
	// Events

	if ($input.length) {
		init($input);
	}

})();
