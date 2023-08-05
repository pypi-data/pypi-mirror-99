/*
    Scripting for the CMS admin.
*/


(function($) {

    /**
     * The main cms plugin. Use by passing in the name of the required method.
     */
    var cms = $.fn.cms = function(method) {
        if (cms[method]) {
            return cms[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else {
            $.error("Method " +  method + " does not exist on jQuery.cms");
        }
    }

    // Namespace for static cms plugins.
    $.cms = {};

    /**
     * Gets the value of a named cookie.
     */
    $.cms.cookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Disables text selection on the given element.
     */
    cms.disableTextSelect = function() {
        return this.each(function() {
    		$(this).mousedown(function() {
    		    return false;
    		});
        });
    }

}(django.jQuery));
