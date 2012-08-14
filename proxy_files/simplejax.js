/**
*
* Copyright (C) 2006  Ed Cradock
*
* This library is free software; you can redistribute it and/or
* modify it under the terms of the GNU Lesser General Public
* License as published by the Free Software Foundation; either
* version 2.1 of the License, or (at your option) any later version.
* 
* This library is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
* Lesser General Public License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with sjInstance.library; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*
* Name : Simplejax Access Library
* Author : Ed Cradock <ed.spam.me+simplejax@gmail.com
* Modified : 10 October 2006
* Version : v1.4
* 
*/
var SIMPLEJAX_FLAG_URL = 1;
var SIMPLEJAX_FLAG_CALLBACK = 2;
var SIMPLEJAX_FLAG_ARGUMENT = 3;
var SIMPLEJAX_FLAG_METHOD = 4;
var SIMPLEJAX_FLAG_FORM = 5;
var SIMPLEJAX_FLAG_FORM_VISIBLE = 6;
var SIMPLEJAX_FLAG_XML = 7;
var SIMPLEJAX_FLAG_JSON = 8;
var SIMPLEJAX_FLAG_NC = 9;
var SIMPLEJAX_FLAG_LOADING = 10;
var SIMPLEJAX_FLAG_HTTPAUTH = 11;
var SIMPLEJAX_FLAG_OPTIONS = 12;

function simplejax(uri, callback, options, errorHandler)
{
   var sjInstance = {};


   if(typeof(errorHandler) == 'function')
      sjInstance.error = errorHandler;
   else
   {
      sjInstance.error = function(status){}
   }

   sjInstance.uri = uri;
   sjInstance.append = '';
   sjInstance.methodType = 'GET';
   sjInstance.postArgs = false;
   sjInstance.returnXML = false;
   sjInstance.json = false;
   sjInstance.nonCached = false;
   sjInstance.authUsername = false;
   sjInstance.authPassword = false;
   sjInstance.options = [];

   sjInstance.callback = callback;
   sjInstance.cbArgs = [];

   sjInstance.source = false;
   sjInstance.http = false;
   sjInstance.req = false;

   sjInstance.construct = function()
   {
      try{sjInstance.req = new ActiveXObject("Microsoft.XMLHTTP");}
      catch(e){sjInstance.req = new XMLHttpRequest()}

      if(sjInstance.req)
      {
         var append = '';
         if(sjInstance.nonCached == true)
         {
            append = ((sjInstance.uri.indexOf('?') != -1) ? '&' : '?' ) + (new Date()).getTime();
         }

         if(sjInstance.authUsername !== false && sjInstance.authPassword !== false)
            sjInstance.req.open(sjInstance.methodType, sjInstance.uri + append , true, sjInstance.authUsername, sjInstance.authPassword);
         else
            sjInstance.req.open(sjInstance.methodType, sjInstance.uri + append, true);

         if(sjInstance.methodType == 'POST')
         {
            sjInstance.req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            var post = true;
         }

         sjInstance.req.send((post == true && sjInstance.postArgs != false) ? sjInstance.postArgs : null);

         post = false; sjInstance.postArgs = false; sjInstance.methodType = 'GET';

         return sjInstance.req;
      }
      else
         sjInstance.error.call(sjInstance, 'Failure to create HTTP Request Object, please use a supported browser.');
   }

   sjInstance.set = function(option, value, argument)
   {
      if(typeof(option) == 'string')
         option = option.toLowerCase(); 

      switch(option)
      {
         case 'url':
         case SIMPLEJAX_FLAG_URL:
            sjInstance.uri = value;
         break;

         case 'callback':
         case SIMPLEJAX_FLAG_CALLBACK:
            sjInstance.callback = value;
         break;

         case 'argument':
         case SIMPLEJAX_FLAG_ARGUMENT:
            sjInstance.cbArgs.push(value);
         break;

         case 'method':
         case SIMPLEJAX_FLAG_METHOD:
            value = value.toUpperCase();
            sjInstance.methodType = (value != 'POST') ? 'GET' : value;
            sjInstance.postArgs = argument;
         break;

         case 'form':
         case 'form-visible':
         case SIMPLEJAX_FLAG_FORM:
         case SIMPLEJAX_FLAG_FORM_VISIBLE:
            var element = document.getElementById(value);
            if(!element)
            {
               sjInstance.error.call(sjInstance, 'Form ' + value + ' does not exist!');
               break;
            }

            var argumentsA = [];
            var elementType;

            for(var i = 0; i <= element.elements.length-1; i++)
            {
               if(element.elements[i].name == '' || element.elements[i].disabled == true) continue;

               if(option == SIMPLEJAX_FLAG_FORM_VISIBLE || option == 'form-visible')
               {
                  if(element.elements[i].style.display == 'none'  || element.elements[i].style.visibility == 'hidden')
                     continue;
               }

               elementType = element.elements[i].type.toLowerCase();
               if(elementType == 'checkbox' || elementType == 'radio')
               {
                  if(element.elements[i].checked != 1)
                     continue;
               }

               argumentsA.push(element.elements[i].name + '=' + escape(element.elements[i].value));
            }

            sjInstance.methodType = element.method.toUpperCase();
            sjInstance.postArgs = argumentsA.join('&');
         break;

         case 'xml':
         case SIMPLEJAX_FLAG_XML:
            sjInstance.returnXML = (value !== true) ? false : value;
         break;

         case 'json':
         case SIMPLEJAX_FLAG_JSON:
            sjInstance.json = (value !== true) ? false : value;
         break;

         case 'non-cached':
         case SIMPLEJAX_FLAG_NC:
            sjInstance.nonCached = (value != true) ? false : value;
         break;

         case 'loading':
         case SIMPLEJAX_FLAG_LOADING:
            sjInstance.loading = value;
         break;

         case 'httpauth':
         case SIMPLEJAX_FLAG_HTTPAUTH:
            sjInstance.authUsername = value;
            sjInstance.authPassword = argument;
         break;

         case 'options':
         case SIMPLEJAX_FLAG_OPTIONS:
            var i;
            for(i in value)
            {
               sjInstance.set(i, value[i]);
            }
         break;

         default:
            sjInstance.error.call(sjInstance, 'Invalid option ' + option);
         break;

         return sjInstance;
      }
   }

   sjInstance.invoke = function()
   {
      for(var i = 0; i <= arguments.length-1; i++)
         sjInstance.cbArgs.push(arguments[i]);

      sjInstance.http = sjInstance.construct();

      if(typeof(sjInstance.http) != undefined)
         sjInstance.http.onreadystatechange = sjInstance.getsource;
      else
         return false;
   }

   sjInstance.abort = function()
   {
      sjInstance.req.abort();
   }

   sjInstance.getsource = function()
   {
      if(sjInstance.http.readyState == 3)
      {
         sjInstance.loading();
      }
      else if(sjInstance.http.readyState == 4)
      {
         if(sjInstance.http.status == 200)
         {
            if(sjInstance.returnXML === true)
               sjInstance.source = sjInstance.http.responseXML;
            else if(sjInstance.json == true && sjInstance.http.responseText.length > 0)
            {
               sjInstance.source = eval('(' + sjInstance.http.responseText + ')');
            }
            else
               sjInstance.source = sjInstance.http.responseText;

            sjInstance.http = false;

            if(sjInstance.cbArgs.length > 0)
            {
               sjInstance.cbArgs.unshift(sjInstance.source);
               sjInstance.callback.apply(sjInstance, sjInstance.cbArgs);
            }else
               sjInstance.callback.call(sjInstance, sjInstance.source);
         }
         else
            sjInstance.error.call(sjInstance, sjInstance.http.status);

         sjInstance.cbArgs = [];
      }
   }

   sjInstance.loading = function() {};

   if(typeof(options) == 'object')
      sjInstance.set('options', options);

   return sjInstance
}
