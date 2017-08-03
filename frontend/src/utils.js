import moment from 'moment';

const DATE_FORMAT = 'MMMM DD, YYYY';

export function formatDate(date) {
    return moment.utc(date).local().format(DATE_FORMAT);
}

export function groupTracks(items) {
    const result = {};

    items.forEach(item => {
        const date = moment.utc(item.date).local();
        const key = date.clone().startOf('day').unix();
        if (!result.hasOwnProperty(key)) {
            result[key] = {date: date.format(DATE_FORMAT), items: []};
        }
        result[key].items.push(item);
        item.time = date.format('HH:mm');
    });

    return Object.keys(result).sort().reverse().map(key => result[key]);
}
