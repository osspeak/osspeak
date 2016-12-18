let modules = {

    setItem: function(moduleMap, data) {
        const moduleCopy = this.copy(moduleMap[data.modulePath]);
        const fieldGroup = moduleCopy[data.type][data.index];
        this.changeNestedProp(fieldGroup, data.fieldKey, data.value);
        moduleMap[data.modulePath] = moduleCopy;
        return moduleMap;
    },

    copy: function(moduleObj) {
        return jQuery.extend(true, {}, moduleObj);
    },

    changeNestedProp: function(obj, key, val) {
        const splitKey = key.split('.');
        for (var i = 0; i < splitKey.length - 1; i++) {
            obj = obj[splitKey[i]];
        }
        obj[splitKey[splitKey.length - 1]] = val;
    }

}