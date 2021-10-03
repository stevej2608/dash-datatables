import React, {Component} from 'react';
import log from 'loglevel';
import PropTypes from 'prop-types';

import 'datatables.net-bs4';

import 'datatables.net-buttons-bs4';
import 'datatables.net-select-bs4';

import 'datatables.net-buttons/js/buttons.colVis';

import 'datatables.net-bs4/css/dataTables.bootstrap4.css';
import 'datatables.net-buttons-bs4/css/buttons.bootstrap4.css'
import 'datatables.net-select-bs4/css/select.bootstrap4.css'

import $ from "jquery";


log.setLevel(log.levels.DEBUG)

function shallow_copy(src) {
  return Object.assign({}, src);
}


const hash_json = function(json, seed = 0) {
    const str = JSON.stringify(json)
    let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
    for (let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1>>>16), 2246822507) ^ Math.imul(h2 ^ (h2>>>13), 3266489909);
    h2 = Math.imul(h2 ^ (h2>>>16), 2246822507) ^ Math.imul(h1 ^ (h1>>>13), 3266489909);
    return 4294967296 * (2097151 & h2) + (h1>>>0);
};


var TABLE_ID = 0;

/**
 * Wrapper for Datatables
 */
export default class DashDatatables extends Component {

  el;
  tableID;
  table_rows

  constructor(props) {
    super(props);
    this.tableID = `react_datatables_${++TABLE_ID}`;
    this.table = null;
    this.buttonBarID = `buttonBar${TABLE_ID}`
    log.info('%s.constructor()', this.tableID);
    this.addButtonAction = this.addButtonAction.bind(this);
    this.editButtonAction = this.editButtonAction.bind(this);
    this.deleteButtonAction = this.deleteButtonAction.bind(this);
    this.filterButtonAction = this.filterButtonAction.bind(this);

    this.table_hash = hash_json(props.data);
    this.submit_count = 0
   }

  /**
   * 
   */

  addButtonAction() {
    log.info('%s.addButtonAction()', this.tableID)
    const submit_count = (++this.submit_count)
    this.props.setProps({ table_event: { action: 'add_row', submit_count }})
  }

  /**
   * 
   */

  editButtonAction(e, dt) {
    log.info('%s.editButtonAction()', this.tableID)
    const submit_count = (++this.submit_count)
    const data = dt.rows({ selected: true }).data()[0];
    this.props.setProps({ table_event: { action: 'edit_row', data: data, submit_count } })
  }

  /**
   * 
   */

  deleteButtonAction(e, dt) {
    log.info('%s.deleteButtonAction()', this.tableID)
    const submit_count = (++this.submit_count)
    const data = dt.rows({ selected: true }).data()[0];
    this.props.setProps({ table_event: { action: 'delete_row', data: data, submit_count } })
  }

  filterButtonAction(e, dt) {
    log.info('%s.filterButtonAction()', this.tableID)
  }

  /**
   * 
   */

  create_datatable() {
    log.debug('%s.create_datatable()', this.tableID)

    // https://datatables.net/reference/option/

    const options = {
      columns: this.props.columns,
      columnDefs: this.props.column_defs,
      pageLength: this.props.pagelength || 10,
    };

    if (this.props.select){
      options.select = this.props.select
    }

    if (this.props.data){
      options.data = this.props.data
    }

    if (this.props.ajax){
      options.ajax = this.props.ajax
    }

    if (this.props.order) {
      options.order = this.props.order;
      options.ordering = true;
    }
    else {
      options.ordering = false;
    }

    if (this.props.editable) {

      // https://datatables.net/reference/option/dom

      options.dom = "<'row'<'col-sm-4'l><'col-sm-3'B><'col-sm-5'f>>" +      // dom for built-in table control elements
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-5'i><'col-sm-7'p>>"

      options.select = {
        style: 'single'
      };

      options.buttons = [

        // https://editor.datatables.net/reference/api/buttons()

        {
          text: 'Add',
          name: 'add',
          className: "btn-sm",
          action: this.addButtonAction

        },

        {
          extend: 'selected',               // Bind to Selected row
          text: 'Edit',
          name: 'edit',
          className: "btn-sm",
          action: this.editButtonAction
        },

        {
          extend: 'selected',                 // Bind to Selected row
          text: 'Delete',
          name: 'delete',
          className: "btn-sm",
          action: this.deleteButtonAction
        },

      ];
    }

    const $el = $(this.el);

    this.table = $el.DataTable(options);
    const props = this.props

    // Handle row selection reporting

    if (props.select) {

      function report_selected(e, dt, type, indexes) {
        if (props.setProps) {
          var indexes = dt.rows( { selected: true } )[0]
          props.setProps({ table_event: { action: 'selectItems', indexes } })
        }       
      }

      this.table.on('select', report_selected);
      this.table.on('deselect', report_selected);

    }

    if (props.column_visibility) {

      // Add Event listeners
      // 
      // https://datatables.net/manual/events
      // https://datatables.net/reference/event/
      // https://datatables.net/reference/event/column-visibility
      
      this.table.on('column-visibility.dt', function (e, settings, column, state) {
        console.log('Column ' + column + ' has changed to ' + (state ? 'visible' : 'hidden'));
        if (props.setProps) {
          const data = { column, state }
          props.setProps({ table_event: { action: 'column-visibility', data: data } })
        }
      });

      // Add the 'Column visibility' dropdown to the button bar
      // 
      // https://datatables.net/extensions/buttons/
      // https://datatables.net/reference/api/buttons()
      // https://datatables.net/extensions/buttons/examples/initialisation/multiple.html
      // https://datatables.net/forums/discussion/30714/problems-initiating-dt-buttons-in-function-executed-via-initcomplete


      new $.fn.dataTable.Buttons(this.table, {
        name: 'primary',
        buttons: [
          {
            extend: 'colvis',
            className: "btn-sm",
          },
          // {
          //   text: 'Filter',
          //   name: 'filter',
          //   className: "btn-sm dropdown-toggle",
          //   action: this.filterButtonAction
          // },

        ]
      });

      this.table.buttons('primary', null).container().prependTo(`#${this.buttonBarID}`);
    }

    log.debug('%s.create_datatable()-done', this.tableID)

  }

  destroy_datatable(){
    if (this.table){
      log.info('%s.destroy_datatable()', this.tableID)
      const table = this.table
      this.table=null
      table.destroy(true)
      log.info('%s.destroy_datatable()-done', this.tableID)
    }
  }

  componentDidUpdate(prevProps) {
    log.debug('%s.componentDidUpdate()', this.tableID)

    if (prevProps.id !== this.props.id){
      log.debug('create table %s', this.props.id)
      this.destroy_datatable();
      this.create_datatable();
      return
    } 


    if (this.props.data) {
      const table_hash = hash_json(this.props.data);
      if (this.table_hash !== table_hash){
        log.debug('table %s rows %d', this.props.id, this.props.data.length)
        this.table_hash = this.table_hash
        this.table.clear().draw();
        this.table.rows.add(this.props.data);
        this.table.columns.adjust().draw();
      }
    }
  }

  /**
   * https://reactjs.org/blog/2018/03/27/update-on-async-rendering.html
   */

  componentDidMount() {
    log.debug('%s.componentDidMount()', this.tableID)
    this.create_datatable();
  }

  /*
   * When the datatables is unmounted, destroy it so that reacts
   * dom manipulation doesn't conflict with jQuery's dom manipulation.
   */

  componentWillUnmount() {
    log.info('%s.componentWillUnmount()', this.tableID)
    this.destroy_datatable()
  }

  table_ref(el) {
    log.info('%s.table_ref()', this.tableID)
    this.el=el
  }

  /**
   * 
   */

  render() {
    const props =  shallow_copy(this.props);
    delete props.editable;
    delete props.data;
    delete props.columns;
    delete props.id;
    delete props.table_event;
    delete props.footer_values;
    delete props.order;
    delete props.data;
    delete props.pagelength;

    const footer = this.props.footer_values;

    const rows = this.props.data? this.props.data.length: 0

    log.info('%s.render() rows=%d', this.tableID, rows)

    return (
      <div id = {this.tableID}>
        <div className="btn-bar" role="group" id={this.buttonBarID}>&nbsp;</div>
        <div className="nbk_sep_s">&nbsp;</div>
        <table
          {...props}
          ref={el => this.table_ref(el)}
        >
          <thead/>
          <tbody/>
          {footer && this.get_footer(footer)}
        </table>
      </div>

    );
  }

}


DashDatatables.defaultProps = {
  editable : false,
  column_visibility : false,
  className : 'table table-sm table-striped table-bordered',
  pagelength : 25
};

DashDatatables.propTypes = {

  /**
   * Load data for the table's content from an Ajax source
   * 
   * https://datatables.net/reference/option/ajax
   */

  ajax: PropTypes.string,

  /**
   * The ID used to identify this component in Dash callbacks
   */
  id: PropTypes.string,

  /**
   * Set `true` to enable row editing
   */

  editable: PropTypes.bool,

  /**
   * Set `true` to enable column visibility control
   */

  column_visibility: PropTypes.bool,

  /**
   * Table data
   */

  data: PropTypes.array,

  /**
   * Column names and attributes
   */

  columns: PropTypes.array,

  /**
   * Allows you to assign specific options to columns 
   * in the table, see:
   * 
   * https://datatables.net/reference/option/columnDefs
   */

  column_defs: PropTypes.array,

  /**
   * Select adds item selection capabilities to a DataTable, see:
   * 
   * https://datatables.net/extensions/select/examples/
   */

  select: PropTypes.array,

  /**
   * Report table events
   */

  table_event: PropTypes.any,

  /**
   * Table footer column values
   */

  footer_values: PropTypes.arrayOf(PropTypes.string),

  /**
   * Sort order
   */
  
  order: PropTypes.array,

  /**
   * Number of rows on a page
   */

  pagelength: PropTypes.number,

  /**
   * Percentage of container to use for table
   */
  
  width: PropTypes.string,

  /**
   * The tables class name
   */

  className: PropTypes.string,

  /**
   * Dash-assigned callback that should be called whenever any of the
   * properties change
   */
  setProps: PropTypes.func
};
