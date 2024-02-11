import type { PageServerLoad } from './$types';
import type { Summoner } from '$lib/types';


// TODO: use env API_HOST and API_HOST when dockerized
export const load: PageServerLoad = async ({ params }) => {
    const res = await fetch(`http://api:8000/summoners`);
    const summoners: Summoner[] = await res.json();

    return {
        props: {
            summoners: summoners
        }
    };
};
