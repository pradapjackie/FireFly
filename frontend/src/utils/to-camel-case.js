import { isPlainObject } from 'lodash';

const toCamel = (s) => {
    return s.replace(/([-_][a-z])/gi, ($1) => {
        return $1.toUpperCase().replace('-', '').replace('_', '');
    });
};

export const toTitle = (s) => {
    return s.charAt(0).toUpperCase() + s.slice(1).replace(/_/g, ' ');
};

export const camelCaseToTitle = (s) => {
    const words = s.match(/[A-Z]?[a-z]+|[A-Z]+(?![a-z])/g);
    return words
        .map((word, index) => (index === 0 ? word.charAt(0).toUpperCase() + word.slice(1) : word.toLowerCase()))
        .join(' ');
};

export function camelize(obj) {
    if (isPlainObject(obj)) {
        const n = {};
        Object.keys(obj).forEach((k) => (n[toCamel(k)] = camelize(obj[k])));
        return n;
    } else if (Array.isArray(obj)) {
        return obj.map((i) => {
            return camelize(i);
        });
    }
    return obj;
}

export function flatCamelize(obj) {
    if (isPlainObject(obj)) {
        const n = {};
        Object.keys(obj).forEach((k) => (n[toCamel(k)] = obj[k]));
        return n;
    } else if (Array.isArray(obj)) obj = obj.map((i) => camelize(i));
    return obj;
}
