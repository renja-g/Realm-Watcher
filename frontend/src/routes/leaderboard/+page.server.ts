import { config } from 'dotenv';
import type { PageServerLoad, Actions } from './$types';
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

// Delete summoner
export const actions = {
    default: async ({ request }) => {
        console.log('Deleting summoner...');
        const data = await request.formData();
        const puuid = data.get('puuid');
        const res = await fetch(`http://${API_HOST}:${API_PORT}/summoners/${puuid}`, {
            method: 'DELETE'
        });
        return {
            status: res.status
        };
    }
} satisfies Actions;
