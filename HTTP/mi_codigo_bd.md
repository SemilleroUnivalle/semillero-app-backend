digraph model_graph {
fontname="Roboto";
fontsize=8;
splines=true;
rankdir="TB";
node [fontname="Roboto", fontsize=8, shape="plaintext"];
edge [fontname="Roboto", fontsize=8];
subgraph cluster_django_contrib_admin {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>django.contrib.admin</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
django_contrib_admin_models_LogEntry [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      LogEntry
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>content_type</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>user</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">action_flag</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">PositiveSmallIntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">action_time</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">change_message</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">object_id</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">object_repr</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_django_contrib_auth {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>django.contrib.auth</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
django_contrib_auth_models_Permission [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Permission
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>content_type</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">codename</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">name</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
django_contrib_auth_models_Group [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Group
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">name</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_django_contrib_contenttypes {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>django.contrib.contenttypes</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
django_contrib_contenttypes_models_ContentType [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      ContentType
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">app_label</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">model</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_django_contrib_sessions {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>django.contrib.sessions</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
django_contrib_sessions_base_session_AbstractBaseSession [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      AbstractBaseSession
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">expire_date</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">session_data</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
django_contrib_sessions_models_Session [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Session<BR/>&lt;<FONT FACE="Roboto"><I>AbstractBaseSession</I></FONT>&gt;
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I><B>session_key</B></I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I><B>CharField</B></I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>expire_date</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>DateTimeField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>session_data</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>TextField</I></FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_rest_framework_authtoken {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>rest_framework.authtoken</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
rest_framework_authtoken_models_Token [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Token
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>key</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>CharField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>user</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">created</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
rest_framework_authtoken_models_TokenProxy [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      TokenProxy
      </B></FONT></TD></TR>
    
      </TABLE>
      >];
}
subgraph cluster_django_rest_passwordreset {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>django_rest_passwordreset</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
django_rest_passwordreset_models_ResetPasswordToken [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      ResetPasswordToken
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>user</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">created_at</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">ip_address</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">GenericIPAddressField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">key</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">user_agent</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_estudiante {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>estudiante</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
estudiante_models_Estudiante [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Estudiante
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_estudiante</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>acudiente</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_acudiente)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_documento_identidad</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_foto</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_informacion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>user</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">apellido</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">area_desempeño</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">celular</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">ciudad_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">colegio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">comuna_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">contrasena</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">departamento_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">descripcion_discapacidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">direccion_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">discapacidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">documento_identidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">email</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">EmailField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">eps</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estamento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">estrato</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">fecha_nacimiento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">foto</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">ImageField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">genero</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">grado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">grado_escolaridad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">is_active</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">numero_documento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">telefono_fijo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tipo_discapacidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tipo_documento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_documento_identidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_foto</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_informacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_acudiente {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>acudiente</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
acudiente_models_Acudiente [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Acudiente
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_acudiente</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">apellido_acudiente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">celular_acudiente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">email_acudiente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre_acudiente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">numero_documento_acudiente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">tipo_documento_acudiente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_area {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>area</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
area_models_Area [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Area
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_area</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado_area</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">imagen_area</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">ImageField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre_area</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_asistencia {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>asistencia</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
asistencia_models_Asistencia [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Asistencia
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_asistencia</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_inscripcion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_inscripcion)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">comentarios</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado_asistencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">fecha_asistencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">sesion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_discapacidad {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>discapacidad</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
discapacidad_models_Discapacidad [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Discapacidad
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_discapacidad</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">info_discapacidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tipo_discapacidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_evaluacion_programa {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>evaluacion_programa</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
evaluacion_programa_models_EvaluacionPrograma [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      EvaluacionPrograma
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_evaluacion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_inscripcion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_inscripcion)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nota_estudiante</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nota_metodologia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nota_monitor</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nota_profesor</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">observaciones</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_grupo {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>grupo</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
grupo_models_Grupo [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Grupo
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>BigAutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>monitor_academico</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (usuario_ptr)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>oferta_academica</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_oferta_academica)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>profesor</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (usuario_ptr)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_historial_cambios {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>historial_cambios</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
historial_cambios_models_HistorialCambios [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      HistorialCambios
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_cambio</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">Observaciones</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_cambio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">id_inscripcion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">IntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">id_modulo_nuevo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">IntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">id_nueva_inscripcion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">IntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">id_periodo_aplazado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">IntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">motivo_cambio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tipo_cambio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_inscripcion {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>inscripcion</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
inscripcion_models_Inscripcion [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Inscripcion
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_inscripcion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_certificado</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_constancia</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_documento_recibo_pago</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_recibo_servicio</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>grupo</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_estudiante</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_estudiante)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_modulo</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_modulo)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_oferta_categoria</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_oferta_categoria)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>oferta_academica</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_oferta_academica)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">certificado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">constancia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_inscripcion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">observaciones</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">recibo_pago</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">recibo_servicio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">terminos</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tipo_vinculacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_certificado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_constancia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_recibo_pago</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_recibo_servicio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_modulo {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>modulo</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
modulo_models_Modulo [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Modulo
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_modulo</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_area</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_area)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_categoria</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_categoria)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">descripcion_modulo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">dirigido_a</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">imagen_modulo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">ImageField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">incluye</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">intensidad_horaria</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">PositiveIntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre_modulo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_pago {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>pago</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
pago_models_Pago [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Pago
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_pago</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_inscripcion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_inscripcion)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">enlace_recibido_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">URLField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">monto</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">referencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_seguimiento_academico {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>seguimiento_academico</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
seguimiento_academico_models_SeguimientoAcademico [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      SeguimientoAcademico
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_seguimiento</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_inscripcion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id_inscripcion)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_ultimo_cambio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nota_conceptual_docente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nota_conceptual_estudiante</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">observaciones</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">seguimiento_1</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">seguimiento_2</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_cuenta {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>cuenta</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
django_contrib_auth_models_AbstractUser [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      AbstractUser<BR/>&lt;<FONT FACE="Roboto"><I>AbstractBaseUser,PermissionsMixin</I></FONT>&gt;
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">date_joined</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">email</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">EmailField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">first_name</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">is_active</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">is_staff</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>is_superuser</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>BooleanField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>last_login</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>DateTimeField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">last_name</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>password</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>CharField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">username</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
cuenta_models_CustomUser [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      CustomUser<BR/>&lt;<FONT FACE="Roboto"><I>AbstractUser</I></FONT>&gt;
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>BigAutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>date_joined</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>DateTimeField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>email</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>EmailField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>first_name</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>CharField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>is_active</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>BooleanField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>is_staff</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>BooleanField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>is_superuser</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>BooleanField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>last_login</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>DateTimeField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>last_name</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><I>CharField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>password</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>CharField</I></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">user_type</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><I>username</I></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><I>CharField</I></FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_administrador {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>administrador</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
administrador_models_Administrador [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Administrador
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_administrador</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>user</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">apellido</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">contrasena</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">correo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">EmailField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_creacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_modificacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">numero_documento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_profesor {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>profesor</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
profesor_models_Profesor [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Profesor
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>usuario_ptr</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_certificado_academico</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_certificado_bancario</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_certificado_laboral</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_documento_identidad</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_foto</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_hoja_vida</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_informacion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_rut</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>modulo</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id_modulo)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">area_desempeño</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">certificado_academico_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">certificado_laboral_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">grado_escolaridad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">hoja_vida_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_certificado_academico</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_certificado_bancario</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_certificado_laboral</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_documento_identidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_foto</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_hoja_vida</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_informacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_rut</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_monitor_academico {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>monitor_academico</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
monitor_academico_models_MonitorAcademico [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      MonitorAcademico
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>usuario_ptr</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_certificado_bancario</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_d10</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_documento_identidad</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_estado_mat_financiera</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_foto</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_informacion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_rut</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_tabulado</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>modulo</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id_modulo)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">area_desempeño</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">d10_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">estado_mat_financiera_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">semestre</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">tabulado_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_certificado_bancario</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_d10</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_documento_identidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_estado_mat_financiera</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_foto</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_informacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_rut</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_tabulado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_monitor_administrativo {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>monitor_administrativo</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
monitor_administrativo_models_MonitorAdministrativo [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      MonitorAdministrativo
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>usuario_ptr</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_certificado_bancario</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_d10</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_documento_identidad</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_estado_mat_financiera</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_foto</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_informacion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_rut</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>audit_tabulado</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">d10_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">estado_mat_financiera_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">tabulado_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_certificado_bancario</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_d10</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_documento_identidad</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_estado_mat_financiera</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_foto</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_informacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_rut</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">verificacion_tabulado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_oferta_academica {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>oferta_academica</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
oferta_academica_models_OfertaAcademica [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      OfertaAcademica
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_oferta_academica</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_desarrollo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">fecha_inicio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_categoria {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>categoria</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
categoria_models_Categoria [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Categoria
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_categoria</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_usuario {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>usuario</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
usuario_models_Usuario [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      Usuario
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>BigAutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>user</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">apellido</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">celular</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">certificado_bancario_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">ciudad_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">comuna_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">contrasena</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">departamento_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">direccion_residencia</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">documento_identidad_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">email</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">EmailField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">eps</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">fecha_nacimiento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">foto</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">ImageField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">genero</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">is_active</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">numero_documento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">rut_pdf</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">FileField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">telefono_fijo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tipo_documento</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_oferta_categoria {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>oferta_categoria</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
oferta_categoria_models_OfertaCategoria [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      OfertaCategoria
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_oferta_categoria</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_categoria</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_categoria)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_oferta_academica</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_oferta_academica)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">fecha_finalizacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">precio_privado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">precio_publico</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">precio_univalle</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">precio_univalle_egresados</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_auditlog {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>auditlog</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
auditlog_models_LogEntry [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      LogEntry
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>actor</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>content_type</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">action</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">PositiveSmallIntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">actor_email</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">additional_data</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">JSONField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">changes</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">JSONField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">changes_text</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">cid</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">object_id</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">BigIntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">object_pk</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">object_repr</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">remote_addr</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">GenericIPAddressField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">remote_port</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">PositiveIntegerField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">serialized_data</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">JSONField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">timestamp</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_prueba_diagnostica {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>prueba_diagnostica</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
prueba_diagnostica_models_PruebaDiagnostica [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      PruebaDiagnostica
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_prueba</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_modulo</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_modulo)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">descripcion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_creacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_modificacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">nombre_prueba</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">puntaje_minimo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tiempo_limite</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">PositiveIntegerField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
prueba_diagnostica_models_PreguntaDiagnostica [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      PreguntaDiagnostica
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_pregunta</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>id_prueba</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto"><B>ForeignKey (id_prueba)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">estado</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">explicacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_creacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_modificacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">imagen</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">ImageField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">puntaje</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">texto_pregunta</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">tipo_pregunta</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">CharField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
prueba_diagnostica_models_RespuestaDiagnostica [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      RespuestaDiagnostica
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_respuesta</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_pregunta</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>ForeignKey (id_pregunta)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">es_correcta</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">BooleanField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_creacion</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto">texto_respuesta</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
subgraph cluster_encuesta_satisfaccion {
label=<
          <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER">
          <FONT FACE="Roboto" COLOR="Black" POINT-SIZE="10">
          <B>encuesta_satisfaccion</B>
          </FONT>
          </TD></TR>
          </TABLE>
          >;
color=olivedrab4;
style="rounded";
encuesta_satisfaccion_models_EncuestaSatisfaccion [label=<
      <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
      <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
      <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
      EncuestaSatisfaccion
      </B></FONT></TD></TR>
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_encuesta</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>AutoField</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT FACE="Roboto"><B>id_inscripcion</B></FONT>
      </TD><TD ALIGN="LEFT">
      <FONT FACE="Roboto"><B>OneToOneField (id_inscripcion)</B></FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">comentarios</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">TextField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_respuesta</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">fecha_ultimo_cambio</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DateTimeField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">nota_docente</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">nota_estudiante</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">nota_modulo</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
    
      <TR><TD ALIGN="LEFT" BORDER="0">
      <FONT COLOR="#7B7B7B" FACE="Roboto">nota_monitor</FONT>
      </TD><TD ALIGN="LEFT">
      <FONT COLOR="#7B7B7B" FACE="Roboto">DecimalField</FONT>
      </TD></TR>
    
    
      </TABLE>
      >];
}
django_contrib_admin_models_LogEntry -> cuenta_models_CustomUser [label=" user (logentry)", arrowhead=none, arrowtail=dot, dir=both];
django_contrib_admin_models_LogEntry -> django_contrib_contenttypes_models_ContentType [label=" content_type (logentry)", arrowhead=none, arrowtail=dot, dir=both];
django_contrib_auth_models_Permission -> django_contrib_contenttypes_models_ContentType [label=" content_type (permission)", arrowhead=none, arrowtail=dot, dir=both];
django_contrib_auth_models_Group -> django_contrib_auth_models_Permission [label=" permissions (group)", arrowhead=dot, arrowtail=dot, dir=both];
django_contrib_sessions_models_Session -> django_contrib_sessions_base_session_AbstractBaseSession [label=" abstract\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
rest_framework_authtoken_models_Token -> cuenta_models_CustomUser [label=" user (auth_token)", arrowhead=none, arrowtail=none, dir=both];
rest_framework_authtoken_models_TokenProxy -> rest_framework_authtoken_models_Token [label=" proxy\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
django_rest_passwordreset_models_ResetPasswordToken -> cuenta_models_CustomUser [label=" user (password_reset_tokens)", arrowhead=none, arrowtail=dot, dir=both];
estudiante_models_Estudiante -> cuenta_models_CustomUser [label=" user (estudiante)", arrowhead=none, arrowtail=none, dir=both];
estudiante_models_Estudiante -> acudiente_models_Acudiente [label=" acudiente (estudiante)", arrowhead=none, arrowtail=dot, dir=both];
estudiante_models_Estudiante -> auditlog_models_LogEntry [label=" audit_documento_identidad (estudiante_documento_identidad)", arrowhead=none, arrowtail=dot, dir=both];
estudiante_models_Estudiante -> auditlog_models_LogEntry [label=" audit_foto (estudiante_foto)", arrowhead=none, arrowtail=dot, dir=both];
estudiante_models_Estudiante -> auditlog_models_LogEntry [label=" audit_informacion (estudiante_informacion)", arrowhead=none, arrowtail=dot, dir=both];
asistencia_models_Asistencia -> inscripcion_models_Inscripcion [label=" id_inscripcion (asistencia)", arrowhead=none, arrowtail=dot, dir=both];
evaluacion_programa_models_EvaluacionPrograma -> inscripcion_models_Inscripcion [label=" id_inscripcion (evaluacionprograma)", arrowhead=none, arrowtail=dot, dir=both];
grupo_models_Grupo -> profesor_models_Profesor [label=" profesor (grupos)", arrowhead=none, arrowtail=dot, dir=both];
grupo_models_Grupo -> monitor_academico_models_MonitorAcademico [label=" monitor_academico (grupo)", arrowhead=none, arrowtail=dot, dir=both];
grupo_models_Grupo -> oferta_academica_models_OfertaAcademica [label=" oferta_academica (grupos)", arrowhead=none, arrowtail=dot, dir=both];
inscripcion_models_Inscripcion -> estudiante_models_Estudiante [label=" id_estudiante (inscripcion)", arrowhead=none, arrowtail=dot, dir=both];
inscripcion_models_Inscripcion -> modulo_models_Modulo [label=" id_modulo (inscripcion)", arrowhead=none, arrowtail=dot, dir=both];
inscripcion_models_Inscripcion -> oferta_categoria_models_OfertaCategoria [label=" id_oferta_categoria (inscripcion)", arrowhead=none, arrowtail=dot, dir=both];
inscripcion_models_Inscripcion -> oferta_academica_models_OfertaAcademica [label=" oferta_academica (inscripcion)", arrowhead=none, arrowtail=dot, dir=both];
inscripcion_models_Inscripcion -> grupo_models_Grupo [label=" grupo (matricula)", arrowhead=none, arrowtail=dot, dir=both];
inscripcion_models_Inscripcion -> auditlog_models_LogEntry [label=" audit_documento_recibo_pago (inscripcion_recibo_pago)", arrowhead=none, arrowtail=none, dir=both];
inscripcion_models_Inscripcion -> auditlog_models_LogEntry [label=" audit_constancia (inscripcion_constancia)", arrowhead=none, arrowtail=none, dir=both];
inscripcion_models_Inscripcion -> auditlog_models_LogEntry [label=" audit_certificado (inscripcion_certificado)", arrowhead=none, arrowtail=none, dir=both];
inscripcion_models_Inscripcion -> auditlog_models_LogEntry [label=" audit_recibo_servicio (inscripcion_recibo_servicio)", arrowhead=none, arrowtail=none, dir=both];
modulo_models_Modulo -> categoria_models_Categoria [label=" id_categoria (modulo_categoria)", arrowhead=none, arrowtail=dot, dir=both];
modulo_models_Modulo -> area_models_Area [label=" id_area (modulo)", arrowhead=none, arrowtail=dot, dir=both];
modulo_models_Modulo -> oferta_categoria_models_OfertaCategoria [label=" id_oferta_categoria (modulo)", arrowhead=dot, arrowtail=dot, dir=both];
pago_models_Pago -> inscripcion_models_Inscripcion [label=" id_inscripcion (pago)", arrowhead=none, arrowtail=dot, dir=both];
seguimiento_academico_models_SeguimientoAcademico -> inscripcion_models_Inscripcion [label=" id_inscripcion (seguimiento)", arrowhead=none, arrowtail=none, dir=both];
django_contrib_auth_base_user_AbstractBaseUser [label=<
  <TABLE BGCOLOR="white" BORDER="0" CELLBORDER="0" CELLSPACING="0">
  <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER" BGCOLOR="#1b563f">
  <FONT FACE="Roboto" POINT-SIZE="12" COLOR="white">AbstractBaseUser</FONT>
  </TD></TR>
  </TABLE>
  >];
django_contrib_auth_models_AbstractUser -> django_contrib_auth_base_user_AbstractBaseUser [label=" abstract\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
django_contrib_auth_models_PermissionsMixin [label=<
  <TABLE BGCOLOR="white" BORDER="0" CELLBORDER="0" CELLSPACING="0">
  <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER" BGCOLOR="#1b563f">
  <FONT FACE="Roboto" POINT-SIZE="12" COLOR="white">PermissionsMixin</FONT>
  </TD></TR>
  </TABLE>
  >];
django_contrib_auth_models_AbstractUser -> django_contrib_auth_models_PermissionsMixin [label=" abstract\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
cuenta_models_CustomUser -> django_contrib_auth_models_Group [label=" groups (user)", arrowhead=dot, arrowtail=dot, dir=both];
cuenta_models_CustomUser -> django_contrib_auth_models_Permission [label=" user_permissions (user)", arrowhead=dot, arrowtail=dot, dir=both];
cuenta_models_CustomUser -> django_contrib_auth_models_AbstractUser [label=" abstract\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
administrador_models_Administrador -> cuenta_models_CustomUser [label=" user (administrador)", arrowhead=none, arrowtail=none, dir=both];
profesor_models_Profesor -> modulo_models_Modulo [label=" modulo (profesores)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_hoja_vida (profesor_d10)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_certificado_laboral (profesor_tabulado)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_certificado_academico (profesor_estado_mat_financiera)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_documento_identidad (profesor_documento_identidad)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_rut (profesor_rut)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_certificado_bancario (profesor_certificado_bancario)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_foto (profesor_foto)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> auditlog_models_LogEntry [label=" audit_informacion (profesor_informacion)", arrowhead=none, arrowtail=dot, dir=both];
profesor_models_Profesor -> usuario_models_Usuario [label=" multi-table\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
monitor_academico_models_MonitorAcademico -> modulo_models_Modulo [label=" modulo (monitor_academico)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_d10 (monitor_academico_d10)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_tabulado (monitor_academico_tabulado)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_estado_mat_financiera (monitor_academico_estado_mat_financiera)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_documento_identidad (monitor_academico_documento_identidad)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_rut (monitor_academico_rut)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_certificado_bancario (monitor_academico_certificado_bancario)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_foto (monitor_academico_foto)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> auditlog_models_LogEntry [label=" audit_informacion (monitor_academico_informacion)", arrowhead=none, arrowtail=dot, dir=both];
monitor_academico_models_MonitorAcademico -> usuario_models_Usuario [label=" multi-table\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_d10 (monitor_administrativo_d10)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_tabulado (monitor_administrativo_tabulado)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_estado_mat_financiera (monitor_administrativo_estado_mat_financiera)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_documento_identidad (monitor_administrativo_documento_identidad)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_rut (monitor_administrativo_rut)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_certificado_bancario (monitor_administrativo_certificado_bancario)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_foto (monitor_administrativo_foto)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> auditlog_models_LogEntry [label=" audit_informacion (monitor_administrativo_informacion)", arrowhead=none, arrowtail=dot, dir=both];
monitor_administrativo_models_MonitorAdministrativo -> usuario_models_Usuario [label=" multi-table\ninheritance", arrowhead=empty, arrowtail=none, dir=both];
usuario_models_Usuario -> cuenta_models_CustomUser [label=" user (usuario)", arrowhead=none, arrowtail=none, dir=both];
oferta_categoria_models_OfertaCategoria -> oferta_academica_models_OfertaAcademica [label=" id_oferta_academica (oferta_academica)", arrowhead=none, arrowtail=dot, dir=both];
oferta_categoria_models_OfertaCategoria -> categoria_models_Categoria [label=" id_categoria (oferta_categoria)", arrowhead=none, arrowtail=dot, dir=both];
auditlog_models_LogEntry -> django_contrib_contenttypes_models_ContentType [label=" content_type (+)", arrowhead=none, arrowtail=dot, dir=both];
auditlog_models_LogEntry -> cuenta_models_CustomUser [label=" actor (+)", arrowhead=none, arrowtail=dot, dir=both];
prueba_diagnostica_models_PruebaDiagnostica -> modulo_models_Modulo [label=" id_modulo (pruebas_diagnosticas)", arrowhead=none, arrowtail=dot, dir=both];
prueba_diagnostica_models_PreguntaDiagnostica -> prueba_diagnostica_models_PruebaDiagnostica [label=" id_prueba (preguntas)", arrowhead=none, arrowtail=dot, dir=both];
prueba_diagnostica_models_RespuestaDiagnostica -> prueba_diagnostica_models_PreguntaDiagnostica [label=" id_pregunta (respuestas)", arrowhead=none, arrowtail=dot, dir=both];
encuesta_satisfaccion_models_EncuestaSatisfaccion -> inscripcion_models_Inscripcion [label=" id_inscripcion (encuesta_satisfaccion)", arrowhead=none, arrowtail=none, dir=both];
}
