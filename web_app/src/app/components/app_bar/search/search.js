

/**
 * A class representing a search query
 */
class SearchQuery {
    /**
     * 
     * @param {string} key - The key to search, or null to search all keys
     * @param {string} query - The query to search for
     */
    constructor(key, query) {
        this.key = key;
        this.query = sanitizeString(query);
    }
}


/**
 * Sanitizes a string for search
 * 
 * @param {string} originalString - The string to sanitize
 * @returns {string} The sanitized string
 * 
 * Removes all non-alphanumeric characters and punctuation, converts all 
 * characters to lowercase, converts all sequences of >1 whitespace to a 
 * single space character, and trims leading and trailing whitespace.
 */
function sanitizeString(originalString) {
    let sanitizedString = originalString.replace(/[^a-zA-Z0-9\s]/g, '');
    sanitizedString = sanitizedString.toLowerCase();
    sanitizedString = sanitizedString.replace(/\s+/g, ' ');
    sanitizedString = sanitizedString.trim();
    return sanitizedString;
}


/**
 * Parses a string into a list of SearchQuery objects
 * 
 * @param {string} originalString - The string to parse
 * @returns {Array.SearchQuery} The parsed phrases
 * 
 * E.g. 'this "is a" title:string description:"to test"' would be parsed to:
 * [
 *      {
 *          key: null,
 *          query: 'this'
 *      },
 *      {
 *          key: null,
 *          query: 'is a'
 *      },
 *      {
 *          key: 'title',
 *          query: 'string'
 *      },
 *      {
 *          key: 'description,
 *          query: 'to test'
 *      },
 * ]
 */
function parseString(originalString) {
    let queries = [];
    (
        originalString.match(
            /[A-Za-z0-9]+:([A-Za-z0-9]+|".*")/g)
        || []
    ).forEach((rawQuery) => {
        let [key, rawString] = rawQuery.split(':');
        let query = new SearchQuery(key, rawString);
        queries.push(query);
        originalString = originalString.replace(rawQuery, ' ');
    });

    (
        originalString.match(/"[^"]*"/g)
        || []
    ).forEach((rawQuery) => {
        let query = new SearchQuery(null, rawQuery);
        queries.push(query);
        originalString = originalString.replace(rawQuery, ' ');
    });

    originalString = originalString.replace(/\s+/g, ' ');

    originalString.split(' ').forEach((rawQuery) => {
        let query = new SearchQuery(null, rawQuery);
        queries.push(query);
        originalString = originalString.replace(rawQuery, ' ');
    });

    queries = queries.filter((query) =>
        typeof query.query === 'string' 
        && query.query.length > 0);

    return queries;
}


/**
 * Duplicates an object and sanitizes all of its string attributes
 * 
 * @param {object} originalObject - The object to duplicate
 * @returns {object} The duplicated and modified object
 */
function createSearchableObj(originalObject) {
    let searchableObject = structuredClone(originalObject);
    searchableObject = Object.fromEntries(
        Object.entries(searchableObject).filter((entry) =>
            typeof entry[1] === 'string')
    );
    Object.keys(searchableObject).forEach(key => {
        let originalValue = searchableObject[key];
        searchableObject[key] = sanitizeString(originalValue);
    });
    return searchableObject;
}


 /**
  * Checks whether an object has an attribute matching a given search query
  * 
  * @param {object} objectToCheck - The object to check
  * @param {Array.SearchQuery} searchQueries - The queries to match against
  * @param {string} searchQuery - The query to match against
  * @returns {boolean} Whether the object matched
  */
function objectMatches(objectToCheck, searchQueries) {
    searchQueries = searchQueries.filter((query) => 
        query.key === null ||
        (
            Object.keys(objectToCheck).includes(query.key)
            && typeof objectToCheck[query.key] === 'string'));

    return searchQueries.some((query) => {
        if (query.key === null) {
            return Object.values(objectToCheck).some((value) =>
                value.includes(query.query));
        }
        else {
            return objectToCheck[query.key].includes(query.query);
        }
    });
}


export { createSearchableObj, objectMatches, parseString };