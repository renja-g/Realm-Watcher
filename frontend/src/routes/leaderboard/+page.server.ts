import { config } from 'dotenv';
import type { PageServerLoad } from './$types';
import type { Summoner } from '$lib/types';


// Load environment variables
config();

// Retrieve environment variables with defaults
const API_HOST = process.env.API_HOST || 'localhost';
const API_PORT = process.env.API_PORT || '8000';

export const load: PageServerLoad = async () => {
    const res = await fetch(`http://${API_HOST}:${API_PORT}/summoners`);
    const summoners: Summoner[] = await res.json();

    return {
        props: {
            summoners: summoners
        }
    };
};
