<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.Loan_ID" placeholder="Loan_ID" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.bank_name" placeholder="bank_name" style="width: 150px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.Loan_Amount" placeholder="Loan_Amount" style="width: 160px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <!-- <el-input v-model="listQuery.Pay_Code" placeholder="Pay_Code" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.Client_ID" placeholder="Client_ID" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" /> -->
      <el-select v-model="listQuery.loan_status" placeholder="loan status" style="width: 120px;margin-left: 10px" class="filter-item">
        <el-option label="not begin" value="not begin"> </el-option>
        <el-option label="in process" value="in process"></el-option>
        <el-option label="finish" value="finish"></el-option>
      </el-select>
      <el-button v-waves class="filter-item" style="margin-left: 10px" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <!-- <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        Export
      </el-button> -->
      <!-- <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        reviewer
      </el-checkbox> -->
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="Loan_ID" prop="Loan_ID" align="center" width="240px" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row[0] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="bank_name" width="300px" align="center">
        <template slot-scope="{row}">
          <span>{{ row[1] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Loan_Amount" width="290px" align="center">
        <template slot-scope="{row}">
          <span>{{ row[2] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="loan_status" width="280px" align="center">
        <template slot-scope="{row}">
          <span>{{ row[3] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="247px" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="success" size="mini" @click="handleDetail(row)">
            Detail
          </el-button>
          <el-button type="primary" size="mini" @click="handlePayLoan(row)">
            Pay
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Loan_ID" prop="Loan_ID">
          <el-input v-model="temp.Loan_ID" />
        </el-form-item>
        <el-form-item label="bank_name" prop="bank_name">
          <el-input v-model="temp.bank_name" />
        </el-form-item>
        <el-form-item label="Loan_Amount" prop="Loan_Amount">
          <el-input v-model="temp.Loan_Amount" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="detailVisible">
      <el-table
        :key="tableKey"
        v-loading="listLoading"
        :data="detail_list"
        border
        fit
        highlight-current-row
        style="width: 100%;"
      >
        <el-table-column label="Pay_Code" prop="Pay_Code" align="center" width="100px">
          <template slot-scope="{row}">
            <span>{{ row[0] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Client_ID" prop="Client_ID" align="center" width="100px">
          <template slot-scope="{row}">
            <span>{{ row[1] }}</span>
          </template>
        </el-table-column>
         <el-table-column label="name" prop="name" align="center" width="120px">
          <template slot-scope="{row}">
            <span>{{ row[4] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="tel" prop="tel" align="center" width="160px">
          <template slot-scope="{row}">
            <span>{{ row[5] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Pay_Amount" prop="Pay_Amount" align="center" width="120px">
          <template slot-scope="{row}">
            <span>{{ row[2] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Pay_Day" prop="Pay_Day" align="center" width="163px">
          <template slot-scope="{row}">
            <span>{{ row[3] }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="PayloanDialogVisible">
      <el-form ref="PayLoandataForm" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Pay_Code" prop="Pay_Code">
          <el-input v-model="temp.Pay_Code" />
        </el-form-item>
        <!-- <el-form-item label="Loan_ID" prop="Loan_ID">
          <el-input v-model="temp.Loan_ID" />
        </el-form-item> -->
        <el-form-item label="Client_ID" prop="Client_ID">
          <el-input v-model="temp.Client_ID" />
        </el-form-item>
        <el-form-item label="Pay_Amount" prop="Pay_Amount">
          <el-input v-model="temp.Pay_Amount" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='payloan'?createPayLoan():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { search_guest, add_guest, delete_guest, update_guest } from '@/api/guest'
import { add_loan, get_loan_list, add_pay_loan, get_loan_detail, delete_loan, search_loan } from '@/api/loan'
const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'Loan',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      detail_list: null,
      data: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        Loan_ID: '',
        bank_name: '',
        Loan_Amount: '',
        Pay_Code: '',
        Client_ID: '',
        pay_state: '',
        loan_status: '',
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      backup_before_update: {
        Client_ID: '',
        name: 'xzwj',
        tel: 10000000000,
        addr: '',
        contact_name: '',
        contact_tel: 10000000000,
        contact_email: '',
        relation: ''
      },
      temp: {
        Loan_ID: '',
        bank_name: '',
        Loan_Amount: '',
        Pay_Code: '',
        Client_ID: '',
        pay_state: '',
        Pay_Code: '',
        Pay_Amount: ''
      },
      dialogFormVisible: false,
      PayloanDialogVisible: false,
      detailVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create',
        payloan: 'Pay Loan',
        detail: 'Loan details'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      var data = {
        Client_ID: '',
        name: '',
        tel: '',
        addr: '',
        contact_name: '',
        contact_tel: '',
        contact_email: '',
        relation: '',
        token: this.$store.getters.token
      }
      console.log(data)
      // console.log('debug 2')
      get_loan_list(data).then(response => {
        console.log(response.data)
        this.list = response.data
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleDetail(row) {
      this.dialogStatus = 'detail'
      this.detailVisible = true
      var data = {
        Loan_ID : row[0]
      }
      get_loan_detail(data).then(response => {
        console.log('loan detail')
        this.detail_list = response.data
        console.log(response.data)
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        // this.dialogFormVisible_1 = false
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      // console.log('debug 1')
      var data = {
        Loan_ID: this.listQuery.Loan_ID,
        bank_name: this.listQuery.bank_name,
        Loan_Amount: this.listQuery.Loan_Amount,
        loan_status: this.listQuery.loan_status
      }
      console.log('handle filter')
      console.log(data)
      // console.log('debug 2')
      search_loan(data).then(response => {
        console.log(response.data)
        this.list = response.data
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        Loan_ID: undefined,
        bank_name: 'ustc-bank',
        Loan_Amount: '1200'
      }
    },
    setTemp(row) {
      this.temp = {
        Client_ID: row[0],
        name: row[1],
        tel: row[2],
        addr: row[3],
        contact_name: row[4],
        contact_tel: row[5],
        contact_email: row[6],
        relation: row[7]
      }
    },
    back_up(row) {
      this.backup_before_update = {
        Client_ID: row[0],
        name: row[1],
        tel: row[2],
        addr: row[3],
        contact_name: row[4],
        contact_tel: row[5],
        contact_email: row[6],
        relation: row[7]
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          var data = {
            Loan_ID: this.temp.Loan_ID,
            bank_name: this.temp.bank_name,
            Loan_Amount: this.temp.Loan_Amount
          }
          console.log(data)
          // console.log('debug 2')
          add_loan(data).then(response => {
            console.log(response.data)
            this.list = response.data
            // this.total = response.data.total
            this.listLoading = false
            // Just to simulate the time of the request
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
            setTimeout(() => {
              this.listLoading = false
            }, 1.5 * 1000)
          })
        }
      })
    },
    handlePayLoan(row) {
      this.temp.Loan_ID = row[0]
      this.dialogStatus = 'payloan'
      this.PayloanDialogVisible = true
      console.log(row)
      this.back_up(row)
      this.$nextTick(() => {
        this.$refs['PayLoandataForm'].clearValidate()
      })
    },
    createPayLoan() {
      this.$refs['PayLoandataForm'].validate((valid) => {
        if (valid) {
          var data = {
            Pay_Code: this.temp.Pay_Code,
            Loan_ID: this.temp.Loan_ID,
            Client_ID: this.temp.Client_ID,
            Pay_Amount: this.temp.Pay_Amount
          }
          console.log(data)
          // console.log('debug 2')
          add_pay_loan(data).then(response => {
            console.log(response.data)
            this.list = response.data
            // this.total = response.data.total
            this.listLoading = false
            // Just to simulate the time of the request
            this.PayloanDialogVisible = false
            this.$notify({
              title: 'Success',
              message: 'Pay Loan Successfully',
              type: 'success',
              duration: 2000
            })
            setTimeout(() => {
              this.listLoading = false
            }, 1.5 * 1000)
          })
        }
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          var data = {
            old_value: this.backup_before_update,
            new_value: this.temp,
          }
          console.log(data)
          // console.log('debug 2')
          update_guest(data).then(response => {
            console.log(response.data)
            this.listLoading = false
            this.list = response.data
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
            setTimeout(() => {
              this.listLoading = false
            }, 1.5 * 1000)
          })
        }
      })
    },
    handleDelete(row, index) {
      this.listLoading = false
      var data = {
        Loan_ID: row[0],
        loan_status: row[3]
      }
      console.log(data)
      // console.log('debug 2')
      delete_loan(data).then(response => {
        console.log(response.data)
        this.list = response.data
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        this.dialogFormVisible = false
        this.$notify({
          title: 'Success',
          message: 'Delete Successfully',
          type: 'success',
          duration: 2000
        })
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
