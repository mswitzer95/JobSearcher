

/**
 * Sanitizes a string for search
 * 
 * @param {string} originalString - The string to sanitize
 * @returns {string} The sanitized string
 * 
 * Removes all non-alphanumeric characters and punctuation, converts all 
 * characters to lowercase, and converts all sequences of >1 whitespace to a 
 * single space character.
 */
function sanitizeString(originalString) {
    let sanitizedString = originalString.replace(/[\W_]+/g, ' ');
    sanitizedString = sanitizedString.toLowerCase();
    sanitizedString = sanitizedString.replace(/\s+/g, ' ');
    return sanitizedString;
}


/**
 * Parses a string into a list of phrases using whitespace and double quotes
 * 
 * @param {string} originalString - The string to parse
 * @returns {Array.string} The parsed phrases
 * 
 * E.g. 'this is "a test" string' would be parsed to:
 * ['this', 'is', 'a test', 'string']
 */
function parseString(originalString) {
    let phrases = originalString.match(/"[^"]*"/g);
    phrases.forEach((phrase) => {
        originalString = originalString.replace(phrase, ' ');
    });
    originalString.split(/\s+/g).forEach((phrase) => {
        phrases.push(phrase);
    });
    phrases = phrases.map(phrase =>
        phrase.replaceAll('"', '').trim());
    phrases = phrases.filter(phrase => phrase.length > 0);
    return phrases;
}


/**
 * Duplicates an object and sanitizes all of its string attributes
 * 
 * @param {object} originalObject - The object to duplicate
 * @returns {object} The duplicated and modified object
 */
function createSearchableObj(originalObject) {
    let searchableObject = structuredClone(originalObject);
    Object.keys(searchableObject).forEach(key => {
        let originalValue = searchableObject[key];
        if (typeof originalValue === 'string') {
            searchableObject[key] = sanitizeString(originalValue);
        }
    });
    return searchableObject;
}


 /**
  * Checks whether an object has an attribute matching a given search query
  * 
  * @param {object} objectToCheck - The object to check
  * @param {Array.<string>} keysToCheck - The object's attributes to check
  * @param {string} searchQuery - The query to match against
  * @returns {boolean} Whether the object matched
  */
function objectMatches(objectToCheck, keysToCheck, searchQuery) {
    keysToCheck = keysToCheck.filter(key =>
        Object.keys(objectToCheck).includes(key)
        && typeof objectToCheck[key] === 'string');
    return keysToCheck.some((key) => objectToCheck[key].includes(searchQuery));
}

export { sanitizeString, createSearchableObj, objectMatches, parseString };