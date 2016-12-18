let modules = {

    setItem: function(moduleMap, data) {
        const moduleCopy = this.copy(moduleMap[data.modulePath]);
        const fieldGroup = moduleCopy[data.type][data.index];
        fieldGroup[data.fieldKey] = data.value;
        moduleMap[data.modulePath] = moduleCopy;
        return moduleMap;
    },

    copy: function(moduleObj) {
        return jQuery.extend(true, {}, moduleObj);
    },

}