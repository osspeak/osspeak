import { NormalizedObjects } from "./types";

export function normalize<T extends {id: string}>(objects: Array<T>): NormalizedObjects<T> {
    const normalized: NormalizedObjects<T> = emptyNormalized();
    for (const obj of objects) {
        normalized.byId[obj.id] = obj;
        normalized.allIds.push(obj.id);
    }
    return normalized
}

export function emptyNormalized() {
    return {byId: {}, allIds: []};
}