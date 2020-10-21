<template>
    <v-dialog
      v-model="dialog"
      max-width="290"
      persistent
    >
      <v-card>
        <v-card-title class="headline">CONSEGUIDO</v-card-title>

        <v-card-text>
          Ya has puntuado las películas necesarias, puedes comenzar a utilizar la aplicación
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="$router.push('/Home')"
          >
            Aceptar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>
<script>
export default {
    name: 'Alerta',
     data: () => ({
         dialog:true
     })
    
}
</script>