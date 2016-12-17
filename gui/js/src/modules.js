let modules = {

    setItem: function(moduleMap, data) {
        const moduleCopy = this.copy(moduleMap[data.modulePath]);
        console.log(data);
    },

    copy: function(moduleObj) {
        return jQuery.extend(true, {}, moduleObj);
    }

}