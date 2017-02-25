let modules = {

    setItem: function(moduleMap, data) {
        const moduleCopy = this.copy(moduleMap[data.modulePath]);
        const changeObj = this.getChangeObj(moduleCopy[data.type][data.index], data);
        changeObj.value = data.value;
        moduleMap[data.modulePath] = moduleCopy;
        return moduleMap;
    },

    copy: function(moduleObj) {
        return jQuery.extend(true, {}, moduleObj);
    },

    getChangeObj: function(fieldObject, data) {
        let changeObj;
        switch (data.type) {
            case 'rules':
                debugger;
                changeObj = [fieldObject.name, fieldObject.value];
                break;
            case 'functions':
                changeObj = [fieldObject.signature, fieldObject.action];
                break;
            case 'commands':
                changeObj = [fieldObject.rule.value, fieldObject.action];
                break;
        }
        return changeObj[data.fieldKey];
    },

}