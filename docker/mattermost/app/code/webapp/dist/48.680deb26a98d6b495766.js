webpackJsonp([48],{1381:function(e,t,a){"use strict";(function(e){function l(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var r=a(51),n=l(r),s=a(32),u=l(s),i=a(33),d=l(i),o=a(50),f=l(o),c=a(49),m=l(c),p=a(197),v=a(1509),E=l(v),_=a(58),g=a(114),h=a(151),y=l(h),N=a(14),M=l(N),b=function(t){function a(e){(0,u.default)(this,a);var t=(0,f.default)(this,(a.__proto__||(0,n.default)(a)).call(this,e));return t.state={verifyStatus:"pending",serverError:""},t}return(0,m.default)(a,t),(0,d.default)(a,[{key:"componentWillMount",value:function(){var e=this;(0,g.verifyEmail)(this.props.location.query.token,function(){_.browserHistory.push("/login?extra=verified&email="+encodeURIComponent(e.props.location.query.email))},function(t){e.setState({verifyStatus:"failure",serverError:t.message})})}},{key:"render",value:function(){return"failure"!==this.state.verifyStatus?M.default.createElement(E.default,null):M.default.createElement("div",null,M.default.createElement("div",{className:"signup-header"},M.default.createElement(_.Link,{to:"/"},M.default.createElement("span",{className:"fa fa-chevron-left"}),M.default.createElement(p.FormattedMessage,{id:"web.header.back"}))),M.default.createElement("div",{className:"col-sm-12"},M.default.createElement("div",{className:"signup-team__container"},M.default.createElement("h3",null,M.default.createElement(p.FormattedMessage,{id:"email_verify.almost",defaultMessage:"{siteName}: You are almost done",values:{siteName:e.window.mm_config.SiteName}})),M.default.createElement("div",null,M.default.createElement("p",null,M.default.createElement(p.FormattedMessage,{id:"email_verify.verifyFailed"})),M.default.createElement("p",{className:"alert alert-danger"},M.default.createElement("i",{className:"fa fa-times"}),this.state.serverError)))))}}]),a}(M.default.Component);t.default=b,b.defaultProps={},b.propTypes={location:y.default.object.isRequired}}).call(t,a(16))},1509:function(e,t,a){"use strict";function l(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var r=a(51),n=l(r),s=a(32),u=l(s),i=a(33),d=l(i),o=a(50),f=l(o),c=a(49),m=l(c),p=a(197),v=a(151),E=l(v),_=a(14),g=l(_),h=function(e){function t(e){(0,u.default)(this,t);var a=(0,f.default)(this,(t.__proto__||(0,n.default)(t)).call(this,e));return a.state={},a}return(0,m.default)(t,e),(0,d.default)(t,[{key:"render",value:function(){var e=g.default.createElement(p.FormattedMessage,{id:"loading_screen.loading",defaultMessage:"Loading"});return this.props.message&&(e=this.props.message),g.default.createElement("div",{className:"loading-screen",style:{position:this.props.position}},g.default.createElement("div",{className:"loading__content"},g.default.createElement("h3",null,e),g.default.createElement("div",{className:"round round-1"}),g.default.createElement("div",{className:"round round-2"}),g.default.createElement("div",{className:"round round-3"})))}}]),t}(g.default.Component);t.default=h,h.defaultProps={position:"relative"},h.propTypes={position:E.default.oneOf(["absolute","fixed","relative","static","inherit"]),message:E.default.node}}});
//# sourceMappingURL=48.680deb26a98d6b495766.js.map