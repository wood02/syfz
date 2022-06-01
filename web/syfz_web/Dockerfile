FROM nginx:1.19 as production-stage

COPY ./nginx/default.conf /etc/nginx/conf.d
COPY ./html/dist /usr/share/nginx/html

#COPY --from=build-stage /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
