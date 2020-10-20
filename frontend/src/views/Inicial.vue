<template>
    <v-container>
        <v-row>
            <v-col cols="3" v-for="item in peliculas" :key="item.id">
                <Pelicula :title="item.title" :id="item.id" :imdbID="item.imdbID" :picture="item.picture" :year="item.year"
                :country="item.country" :director="item.director" :actors="item.actors" :genre="item.genre"></Pelicula>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import Pelicula from "@/components/Pelicula.vue";

export default{
    name: "Inicial",
    components: {
        Pelicula
    },
    data: () => ({
        peliculas : [{
            id : 11,
            title : 'Jumanji',
            imdbID: "0113497",
            picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
            country: "USA",
            director: "Joe Johnston",
            actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
            genre: ["Adventure", "Fantasy", "Children"],
            year:2010
        },
        {
            id : 804,
            title : 'Ella es unica',
            imdbID: "0117628",
            picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
            country: "USA",
            director: "Joe Johnston",
            actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
            genre: ["Adventure", "Fantasy", "Children"],
            year: 2000
        },
        {
            id : 3239,
            title : 'Ella es unica',
            imdbID: "0141399",
            picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
            country: "USA",
            director: "Joe Johnston",
            actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
            genre: ["Adventure", "Fantasy", "Children"],
            year: 1980
        },
        {
            id : 11,
            title : 'Jumanji',
            imdbID: "0113497",
            picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
            country: "USA",
            director: "Joe Johnston",
            actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
            genre: ["Adventure", "Fantasy", "Children"],
            year:2010
        },
        {
            id : 804,
            title : 'Ella es unica',
            imdbID: "0117628",
            picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
            country: "USA",
            director: "Joe Johnston",
            actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
            genre: ["Adventure", "Fantasy", "Children"],
            year: 2000
        },
        {
            id : 3239,
            title : 'Ella es unica',
            imdbID: "0141399",
            picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
            country: "USA",
            director: "Joe Johnston",
            actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
            genre: ["Adventure", "Fantasy", "Children"],
            year: 1980
        }
        ]
    })
    }
</script>