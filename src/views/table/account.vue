<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.Client_ID" placeholder="id" style="width: 50px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.name" placeholder="name" style="width: 80px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.tel" placeholder="tel" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.addr" placeholder="addr" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.contact_name" placeholder="con_name" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.contact_tel" placeholder="con_addr" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.contact_email" placeholder="con_email" style="width: 200px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.relation" placeholder="relation" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.bank_name" placeholder="bank_name" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.account_id" placeholder="account_id" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.balance" placeholder="balance" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.opendate" placeholder="opendate" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.recent_visit_date" placeholder="recent_visit_date" style="width: 180px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.count_type" placeholder="count_type" style="width: 120px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate_1">
        Add Saving
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate_2">
        Add Checking
      </el-button>
      <!-- <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        Export
      </el-button> -->
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 95%;"
    >
      <el-table-column label="Client_ID" prop="id" align="center" width="152px">
        <template slot-scope="{row}">
          <span>{{ row[0] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="name" prop="name" align="center" width="170px">
        <template slot-scope="{row}">
          <span>{{ row[1] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="bank_name" prop="bank_name" width="182px" align="center">
        <template slot-scope="{row}">
          <span>{{ row[2] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="account_id" prop="account_id" width="181px" align="center">
        <template slot-scope="{row}">
          <span>{{ row[3] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="balance" prop="balance" width="180px" align="center">
        <template slot-scope="{row}">
          <span>{{ row[4] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="count_type" prop="count_type" width="181px" align="center">
        <template slot-scope="{row}">
          <span>{{ row[5] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="success" size="mini" @click="handleDetail(row)">
            Detail
          </el-button>
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            Edit
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible_1">
      <el-form ref="dataForm1" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Client_ID" prop="id">
          <el-input v-model="temp.Client_ID" />
        </el-form-item>
        <el-form-item label="account_id" prop="account_id">
          <el-input v-model="temp.account_id" />
        </el-form-item>
        <el-form-item label="bank_name" prop="bank_name">
          <el-input v-model="temp.bank_name" />
        </el-form-item>
        <el-form-item label="balance" prop="balance" type='Number'>
          <el-input v-model="temp.balance" />
        </el-form-item>
        <el-form-item label="interest_rate" prop="interest_rate" type='Number'>
          <el-input v-model="temp.interest_rate" />
        </el-form-item>
        <el-form-item label="currency_type" prop="currency_type">
          <el-input v-model="temp.currency_type" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_1 = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create_saving'?createData_1():updateData_1()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible_2">
      <el-form ref="dataForm2" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Client_ID" prop="id">
          <el-input v-model="temp.Client_ID" />
        </el-form-item>
        <el-form-item label="account_id" prop="account_id">
          <el-input v-model="temp.account_id" />
        </el-form-item>
        <el-form-item label="bank_name" prop="bank_name">
          <el-input v-model="temp.bank_name" />
        </el-form-item>
        <el-form-item label="balance" prop="balance" type='Number'>
          <el-input v-model="temp.balance" />
        </el-form-item>
        <el-form-item label="over_draft" prop="over_draft" type='Number'>
          <el-input v-model="temp.over_draft" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_2 = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create_checking'?createData_2():updateData_2()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible_3">
      <el-table
        :key="tableKey"
        v-loading="listLoading"
        :data="detail_list"
        border
        fit
        highlight-current-row
        style="width: 100%;"
      >
        <el-table-column label="attribute" prop="attribute" align="center" width="223px">
          <template slot-scope="{row}">
            <span>{{ row[0] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="value" prop="value" align="center" width="540px">
          <template slot-scope="{row}">
            <span>{{ row[1] }}</span>
          </template>
        </el-table-column>
      </el-table>
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
import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { add_saving_account, add_checking_account, search_account, delete_account, get_account_info } from '@/api/account'
import { update_saving_account, update_checking_account, get_user_account_detail } from '@/api/account'

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
  name: 'Account',
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
      total: 0,
      listLoading: true,
      listQuery: {
        Client_ID: '',
        name: '',
        tel: '',
        addr: '',
        contact_name: '',
        contact_tel: '',
        contact_email: '',
        relation: '',
        bank_name: '',
        account_id: '',
        balance: '',
        opendate: '',
        recent_visit_date: '',
        count_type: '',
        interest_rate: '',
        currency_type: '',
        over_draft: '',
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        Client_ID: '',
        name: '',
        tel: '',
        addr: '',
        contact_name: '',
        contact_tel: '',
        contact_email: '',
        relation: '',
        bank_name: '',
        account_id: '',
        balance: '',
        opendate: '',
        recent_visit_date: '',
        count_type: '',
        interest_rate: '',
        currency_type: '',
        over_draft: '',
        sort: '+id'
      },
      back_up_before_update: {
        Client_ID: '',
        name: '',
        tel: '',
        addr: '',
        contact_name: '',
        contact_tel: '',
        contact_email: '',
        relation: '',
        bank_name: '',
        account_id: '',
        balance: '',
        opendate: '',
        recent_visit_date: '',
        count_type: '',
        interest_rate: '',
        currency_type: '',
        over_draft: '',
        sort: '+id'
      },
      dialogFormVisible_1: false,
      dialogFormVisible_2: false,
      dialogFormVisible_3: false,
      dialogFormVisible_4: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create_checking: 'Create checking account',
        create_saving: 'Create saving account',
        show_detail: 'Account Details'
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
      var data = {
        Client_ID: '',
        name: '',
        tel: '',
        addr: '',
        contact_name: '',
        contact_tel: '',
        contact_email: '',
        relation: '',
        bank_name: '',
        account_id: '',
        balance: '',
        open_date: '',
        recent_visit_date: '',
        count_type: ''
      }
      console.log(data)
      search_account(data).then(response => {
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
    handleFilter() {
      var data = {
        Client_ID: this.listQuery.Client_ID,
        name: this.listQuery.name,
        tel: this.listQuery.tel,
        addr: this.listQuery.addr,
        contact_name: this.listQuery.contact_name,
        contact_tel: this.listQuery.contact_tel,
        contact_email: this.listQuery.contact_email,
        relation: this.listQuery.relation,
        bank_name: this.listQuery.bank_name,
        account_id: this.listQuery.account_id,
        balance: this.listQuery.balance,
        open_date: this.listQuery.opendate,
        recent_visit_date: this.listQuery.recent_visit_date,
        count_type: this.listQuery.count_type
      }
      console.log(data)
      search_account(data).then(response => {
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
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
    },
    resetTemp() {
      this.temp = {
        Client_ID: '',
        name: 'xzwj',
        tel: '13255561448',
        addr: 'ustc',
        contact_name: 'xsa',
        contact_tel: 'csac',
        contact_email: 'cas',
        relation: 'csa',
        bank_name: 'ustc-bank',
        account_id: '',
        balance: '1200',
        opendate: '',
        recent_visit_date: '',
        count_type: '',
        interest_rate: '0.12',
        currency_type: 'dollar',
        over_draft: '1200',
        sort: '+id'
      }
    },
    handleDetail(row) {
      this.dialogStatus = 'show_detail'
      this.dialogFormVisible_3 = true
      var data = {
        Client_ID : row[0],
        account_id: row[3],
        count_type: row[5]
      }
      get_user_account_detail(data).then(response => {
        console.log('account detail')
        console.log(response)
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
    handleCreate_1() {
      this.resetTemp()
      this.dialogStatus = 'create_saving'
      this.dialogFormVisible_1 = true
      this.$nextTick(() => {
        this.$refs['dataForm1'].clearValidate()
      })
    },
    createData_1() {
      this.$refs['dataForm1'].validate((valid) => {
        if (valid) {
          var data = {
            Client_ID: this.temp.Client_ID,
            account_id: this.temp.account_id,
            bank_name: this.temp.bank_name,
            balance: this.temp.balance,
            interest_rate: this.temp.interest_rate,
            currency_type: this.temp.currency_type
          }
          console.log(data)
          add_saving_account(data).then(response => {
            console.log(response.data)
            this.list = response.data
            // this.total = response.data.total
            this.listLoading = false
            // Just to simulate the time of the request
            this.dialogFormVisible_1 = false
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
    handleCreate_2() {
      this.resetTemp()
      this.dialogStatus = 'create_checking'
      this.dialogFormVisible_2 = true
      this.$nextTick(() => {
        this.$refs['dataForm2'].clearValidate()
      })
    },
    createData_2() {
      this.$refs['dataForm2'].validate((valid) => {
        if (valid) {
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          var data = {
            Client_ID: this.temp.Client_ID,
            account_id: this.temp.account_id,
            bank_name: this.temp.bank_name,
            balance: this.temp.balance,
            over_draft: this.temp.over_draft
          }
          console.log('in add checking account in vue file')
          console.log(data)
          add_checking_account(data).then(response => {
            console.log(response.data)
            this.list = response.data
            // this.total = response.data.total
            this.listLoading = false
            // Just to simulate the time of the request
            this.dialogFormVisible_2 = false
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
    handleUpdate(row) {
      if(row[5] == 0){
        this.handleUpdate_1(row)
      }
      else if(row[5] == 1){
        this.handleUpdate_2(row)
      }
    },
    handleUpdate_1(row) {
      var data = {
        Client_ID: row[0],
        account_id: row[3],
        count_type: row[5]
      }
      get_account_info(data).then(response => {
        this.temp.Client_ID = row[0]
        this.temp.account_id = row[3]
        this.temp.bank_name = row[2]
        this.temp.balance = row[4]
        this.temp.interest_rate = response.data[0][1]
        this.temp.currency_type = response.data[0][2]
        this.back_up_before_update.Client_ID = row[0]
        this.back_up_before_update.account_id = row[3]
        this.back_up_before_update.bank_name = row[2]
        this.back_up_before_update.balance = row[4]
        this.back_up_before_update.interest_rate = response.data[0][1]
        this.back_up_before_update.currency_type = response.data[0][2]
      })
      this.dialogStatus = 'update'
      this.dialogFormVisible_1 = true
      this.$nextTick(() => {
        this.$refs['dataForm1'].clearValidate()
      })
    },
    updateData_1() {
      this.$refs['dataForm1'].validate((valid) => {
        if (valid) {
          var data = {
            old_value: this.back_up_before_update,
            new_value: this.temp
          }
          update_saving_account(data).then(response => {
            console.log(response.data)
            this.listLoading = false
            this.list = response.data
            this.dialogFormVisible_1 = false
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
    handleUpdate_2(row) {
      var data = {
        Client_ID: row[0],
        account_id: row[3],
        count_type: row[5]
      }
      get_account_info(data).then(response => {
        this.temp.Client_ID = row[0]
        this.temp.account_id = row[3]
        this.temp.bank_name = row[2]
        this.temp.balance = row[4]
        this.temp.over_draft = response.data[0][1]
        this.back_up_before_update.Client_ID = row[0]
        this.back_up_before_update.account_id = row[3]
        this.back_up_before_update.bank_name = row[2]
        this.back_up_before_update.balance = row[4]
        this.back_up_before_update.over_draft = response.data[0][1]
      })
      this.dialogStatus = 'update'
      this.dialogFormVisible_2 = true
      this.$nextTick(() => {
        this.$refs['dataForm2'].clearValidate()
      })
    },
    updateData_2() {
      this.$refs['dataForm2'].validate((valid) => {
        if (valid) {
          var data = {
            old_value: this.back_up_before_update,
            new_value: this.temp
          }
          update_checking_account(data).then(response => {
            console.log(response.data)
            this.listLoading = false
            this.list = response.data
            this.dialogFormVisible_2 = false
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
      var data = {
        Client_ID: row[0],
        name: row[1],
        bank_name: row[2],
        account_id: row[3],
        balance: row[4],
        count_type: row[5]
      }
      delete_account(data).then(response => {
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
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
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